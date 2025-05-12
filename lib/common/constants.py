portfolio_label = 'Portfolio'

class Time:
    millis_in_second = 1000
    millis_in_minute = 60 * millis_in_second
    millis_in_hour = 60 * millis_in_minute
    millis_in_day = 24 * millis_in_hour
    millis_in_week = 7 * millis_in_day
    millis_in_month = 30 * millis_in_day


class Url:

    buildship = 'https://iupixp.buildship.run/theezy-trader'
    portfolio = '/portfolio'
    contribute = '/portfolio/contribute'
    follow = '/portfolio/follow'
    unfollow = '/portfolio/unfollow'
    members = '/portfolio/members'
    portfolio_search = '/portfolio/search'

    account_deposit = '/account/deposit-funds'
    account_balance = '/account/balance'

    stock_details = '/stocks/details'
    stock_by_portfolio = '/stocks/portfolio'
    stock_search = '/stocks/search'
    stock_purchase = '/stocks/purchase'
    stock_sell = '/stocks/sell'

    transactions = '/transactions'


    polygon = 'https://api.polygon.io'
    stock_quotes = '/v3/quotes/'
    stock_aggregates = '/v2/aggs/ticker/{}/range/1/{}/{}/{}'
    stock_weekly_aggregates = '/v2/aggs/ticker/{}/range/1/week/{}/{}'
    stock_monthly_aggregates = '/v2/aggs/ticker/{}/range/1/month/{}/{}'
    stock_yearly_aggregates = '/v2/aggs/ticker/{}/range/1/year/{}/{}'
    stock_tickers = '/v3/reference/tickers'
    stock_ticker_snapshots = '/v2/snapshot/locale/us/markets/stocks/tickers'

urls = Url()
time = Time()