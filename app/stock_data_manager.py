import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
from functools import lru_cache

class StockDataManager:
    def __init__(self):
        self.stock_data_path = "data/stock_data.json"
        self.mf_data_path = "data/mutual_funds_data.json"
        self.mf_holdings_path = "data/mf_holdings_data.json"
        self.stock_data: Dict[str, Any] = {}
        self.mf_data: Dict[str, Any] = {}
        self.mf_holdings: Dict[str, Any] = {}
        self._load_data()

    def _load_data(self) -> None:
        """Load data from JSON files if they exist."""
        try:
            if os.path.exists(self.stock_data_path):
                with open(self.stock_data_path, 'r') as f:
                    self.stock_data = json.load(f)
            
            if os.path.exists(self.mf_data_path):
                with open(self.mf_data_path, 'r') as f:
                    self.mf_data = json.load(f)
            
            if os.path.exists(self.mf_holdings_path):
                with open(self.mf_holdings_path, 'r') as f:
                    self.mf_holdings = json.load(f)
        except Exception as e:
            print(f"Error loading data: {str(e)}")

    @lru_cache(maxsize=100)
    def get_stock_metrics(self, symbol: str) -> Dict[str, Any]:
        """Get metrics for a specific stock."""
        return self.stock_data.get(symbol, {})

    @lru_cache(maxsize=50)
    def get_sector_performance(self, sector: str) -> Dict[str, float]:
        """Get performance metrics for a specific sector."""
        sector_stocks = {
            symbol: data for symbol, data in self.stock_data.items()
            if data.get('sector') == sector
        }
        
        if not sector_stocks:
            return {}

        return {
            'avg_returns': sum(stock['returns'] for stock in sector_stocks.values()) / len(sector_stocks),
            'market_cap': sum(stock['market_cap'] for stock in sector_stocks.values()),
            'volume': sum(stock['volume'] for stock in sector_stocks.values())
        }

    def get_relevant_funds(self, symbol: str = None, sector: str = None) -> List[Dict[str, Any]]:
        """Get relevant mutual funds based on stock or sector."""
        relevant_funds = []
        
        if symbol:
            # Find funds holding this stock
            relevant_funds.extend([
                {
                    'fund_name': fund_name,
                    'allocation': fund_data['holdings'].get(symbol, 0),
                    'nav': fund_data.get('nav', 0),
                    'returns': fund_data.get('returns', 0)
                }
                for fund_name, fund_data in self.mf_data.items()
                if symbol in fund_data.get('holdings', {})
            ])
        
        if sector:
            # Find sector-focused funds
            relevant_funds.extend([
                {
                    'fund_name': fund_name,
                    'sector_exposure': fund_data.get('sector_allocation', {}).get(sector, 0),
                    'nav': fund_data.get('nav', 0),
                    'returns': fund_data.get('returns', 0)
                }
                for fund_name, fund_data in self.mf_data.items()
                if fund_data.get('sector_allocation', {}).get(sector, 0) > 20  # >20% exposure
            ])
        
        return sorted(relevant_funds, key=lambda x: x.get('returns', 0), reverse=True)[:5]

    def get_focused_analysis(self, query: str) -> Dict[str, Any]:
        """Get focused analysis based on the query."""
        # Extract symbols and sectors from query
        words = query.upper().split()
        symbols = [word for word in words if word in self.stock_data]
        sectors = [word.title() for word in words if word.title() in self._get_all_sectors()]
        
        analysis = {
            'query_focus': query,
            'timestamp': datetime.now().isoformat()
        }

        if symbols:
            symbol = symbols[0]  # Focus on the first mentioned symbol
            stock_data = self.get_stock_metrics(symbol)
            analysis.update({
                'stock_data': {
                    'symbol': symbol,
                    'current_price': stock_data.get('price'),
                    'change_percent': stock_data.get('returns'),
                    'volume': stock_data.get('volume')
                },
                'related_funds': self.get_relevant_funds(symbol=symbol)
            })

        if sectors:
            sector = sectors[0]  # Focus on the first mentioned sector
            sector_data = self.get_sector_performance(sector)
            analysis.update({
                'sector_data': {
                    'name': sector,
                    'performance': sector_data.get('avg_returns'),
                    'market_cap': sector_data.get('market_cap')
                },
                'sector_funds': self.get_relevant_funds(sector=sector)
            })

        return analysis

    @lru_cache(maxsize=1)
    def _get_all_sectors(self) -> List[str]:
        """Get list of all sectors."""
        return list(set(stock.get('sector') for stock in self.stock_data.values() if stock.get('sector')))

    def get_market_summary(self) -> Dict[str, Any]:
        """Get overall market summary."""
        if not self.stock_data:
            return {}

        total_market_cap = sum(stock['market_cap'] for stock in self.stock_data.values())
        avg_pe = sum(stock['pe_ratio'] for stock in self.stock_data.values()) / len(self.stock_data)
        
        return {
            'total_market_cap': total_market_cap,
            'average_pe': avg_pe,
            'stock_count': len(self.stock_data),
            'sectors': list(set(stock['sector'] for stock in self.stock_data.values())),
            'top_gainers': self._get_top_movers(limit=5, ascending=False),
            'top_losers': self._get_top_movers(limit=5, ascending=True)
        }

    def _get_top_movers(self, limit: int = 5, ascending: bool = True) -> List[Dict[str, Any]]:
        """Get top gaining or losing stocks."""
        sorted_stocks = sorted(
            [{'symbol': k, **v} for k, v in self.stock_data.items()],
            key=lambda x: x['returns'],
            reverse=not ascending
        )
        return sorted_stocks[:limit]

    def get_stock_recommendation(self, symbol: str) -> Dict[str, Any]:
        """Get stock recommendation based on technical and fundamental analysis."""
        stock = self.stock_data.get(symbol)
        if not stock:
            return {}

        # Calculate basic metrics
        pe_ratio = stock['pe_ratio']
        avg_sector_pe = sum(s['pe_ratio'] for s in self.stock_data.values() 
                          if s['sector'] == stock['sector']) / len(self.stock_data)
        
        return {
            'symbol': symbol,
            'current_price': stock['price'],
            'pe_ratio': pe_ratio,
            'sector_avg_pe': avg_sector_pe,
            'market_cap': stock['market_cap'],
            'recommendation': 'BUY' if pe_ratio < avg_sector_pe else 'HOLD',
            'confidence': min(100, max(0, int((avg_sector_pe - pe_ratio) / avg_sector_pe * 100))),
            'technical_indicators': {
                'rsi': stock.get('rsi', 0),
                'macd': stock.get('macd', 0),
                'volume': stock.get('volume', 0)
            }
        }

# Initialize the manager
stock_manager = StockDataManager() 