import numpy as np
import pandas as pd


def eval_strategy(x):

    df =x

    bot = Bot(df)
    bot.trade()

    profit, win_rate = bot.get_profit(), bot.get_win_rate()


    return profit, win_rate


class Bot:
    """
    This class provide tradding management and work with sell and buy condition.

    input:
        - df: pd.DataFrame
                columns=['close', 'signal'],
                signal=[-1, 0, 1] such that : -1: buy, 0: hold, 1: sell
    """

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.df['signal'] = self.df['signal'].astype(float)
        self.trades = list()
        self.in_trade = False

    def trade(self):
        """ trade function work with signal """

        for i in self.df.index:
            # buy
            if self.df.loc[i, 'signal'] == -1 and not self.in_trade:

                position = dict()
                position[i] = self.df.loc[i, 'close']
                self.in_trade = True
            # sell
            elif self.df.loc[i, 'signal'] == 1 and self.in_trade:

                position[i] = self.df.loc[i, 'close']
                self.trades.append(position)
                self.in_trade = False
            # hold
            elif self.df.loc[i, 'signal'] == 0:
                continue

    def get_win_rate(self):
        return np.round(sum(
            [1 if list(pos.values())[0] < list(pos.values())
             [1] else 0 for pos in self.trades]
        ) / len(self.trades), 4)

    def get_profit(self):

        profit = 1
        for pos in self.trades:
            cl = np.array(list(pos.values()))
            profit *= cl[1:] / cl[:-1] - 0.0125

        return np.round(profit[0], 4)

    def __len__(self):
        return len(self.trades)

    def __repr__(self):
        return f"<WinRate: {self.get_win_rate()}, Profit: {self.get_profit()}>"

if __name__ == "__main__":
    profit, win_rate = eval_strategy()
    print("profit:", profit,"\nwin_rate:", win_rate)
