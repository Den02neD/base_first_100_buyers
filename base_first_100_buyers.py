import requests, time

def first_100_buyers():
    print("Base — First 100 Buyers Tracker (live leaderboard of earliest apes)")
    # pairAddress → {wallet: amount_usd}
    leaderboards = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=500")
            for tx in r.json().get("transactions", []):
                pair = tx["pairAddress"]
                if pair not in leaderboards:
                    leaderboards[pair] = {}

                # Only count buys (not sells)
                if tx.get("side") != "buy":
                    continue

                wallet = tx["from"]
                usd = tx.get("valueUSD", 0)

                # Age filter — only tokens < 10 min old
                age = time.time() - tx.get("timestamp", 0)
                if age > 600:
                    continue

                # Add or update wallet
                leaderboards[pair][wallet] = leaderboards[pair].get(wallet, 0) + usd

                # Print live leaderboard when 100 unique buyers reached
                if len(leaderboards[pair]) >= 100 and len(leaderboards[pair]) <= 105:
                    token = tx["token0"]["symbol"] if tx["token0"]["address"] != "0x4200000000000000000000000000000000000006" else tx["token1"]["symbol"]
                    top5 = sorted(leaderboards[pair].items(), key=lambda x: -x[1])[:5]

                    print(f"FIRST 100 BUYERS REACHED — {token}\n"
                          f"Total unique apes: {len(leaderboards[pair])}\n"
                          f"Top 5 earliest & biggest:\n")
                    for i, (w, a) in enumerate(top5, 1):
                        print(f"  {i}. {w[:10]}... → ${a:,.0f}")
                    print(f"https://dexscreener.com/base/{pair}\n"
                          f"→ These are the real OGs. Everyone else is late.\n"
                          f"{'='*90}")

        except:
            pass
        time.sleep(1.9)

if __name__ == "__main__":
    first_100_buyers()
