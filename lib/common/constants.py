portfolio_label = 'Portfolio'

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
    stock_daily_aggregates = '/v2/aggs/ticker/{}/range/1/day/{}/{}'
    stock_tickers = '/v3/reference/tickers'
    stock_ticker_snapshots = '/v2/snapshot/locale/us/markets/stocks/tickers'

urls = Url()