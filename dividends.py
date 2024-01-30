import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def calculate_and_compare_investment_strategies(ticker_symbol, period, initial_investment, annual_yield):
    """
    Calculate and compare three investment strategies: 
    1) With dividend reinvestment, 
    2) Without dividend reinvestment, 
    3) SPY (S&P 500 ETF) growth.
    """
    def fetch_and_calculate(ticker, yield_rate=None, reinvest_dividends=True):

        price_data = yf.download(ticker, period=f"{period}y", interval='1mo')
        price_data.index = price_data.index.tz_localize(None)
        price_data = price_data.resample('M').last()

        investment_value = pd.DataFrame(index=price_data.index)
        investment_value['Shares'] = 0.0
        initial_share_price = price_data.iloc[0]['Close']
        initial_shares = initial_investment / initial_share_price
        investment_value.at[investment_value.index[0], 'Shares'] = initial_shares

        
        for month in investment_value.index[1:]:
            previous_month = investment_value.index[investment_value.index.get_loc(month) - 1]
            previous_shares = investment_value.at[previous_month, 'Shares']
            monthly_dividend_per_share = (yield_rate * price_data.at[month, 'Close']) / 12 if yield_rate else 0
            total_dividends = monthly_dividend_per_share * previous_shares if reinvest_dividends else 0
            reinvested_shares = total_dividends / price_data.at[month, 'Close']
            investment_value.at[month, 'Shares'] = previous_shares + reinvested_shares
        investment_value['Total Value'] = investment_value['Shares'] * price_data['Close']
        return investment_value

    def display_summary_statistics(investment_value, description):
        final_value = investment_value['Total Value'].iloc[-1]
        total_growth = final_value - initial_investment
        average_annual_growth = (final_value / initial_investment) ** (1/period) - 1
        print(f"\nSummary for {description}:")
        print(f"Initial Investment: ${initial_investment}")
        print(f"Final Investment Value: ${final_value:.2f}")
        print(f"Total Growth: ${total_growth:.2f}")
        print(f"Average Annual Growth Rate: {average_annual_growth:.2%}")

    ticker_investment_reinvest = fetch_and_calculate(ticker_symbol, annual_yield)
    ticker_investment_no_reinvest = fetch_and_calculate(ticker_symbol, annual_yield, reinvest_dividends=False)
    spy_investment = fetch_and_calculate("SPY")
    plt.figure(figsize=(12, 6))
    plt.plot(ticker_investment_reinvest['Total Value'], label=f'{ticker_symbol} with Dividend Reinvestment')
    plt.plot(ticker_investment_no_reinvest['Total Value'], label=f'{ticker_symbol} without Dividend Reinvestment')
    plt.plot(spy_investment['Total Value'], label='SPY Growth')
    plt.title(f'Investment Strategy Comparison Over {period} Years')
    plt.xlabel('Date')
    plt.ylabel('Total Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()
    display_summary_statistics(ticker_investment_reinvest, f"{ticker_symbol} with Dividend Reinvestment")
    display_summary_statistics(ticker_investment_no_reinvest, f"{ticker_symbol} without Dividend Reinvestment")
    display_summary_statistics(spy_investment, "SPY Growth")


calculate_and_compare_investment_strategies("BST", 10, 10000, 0.09)
