import nextcord, random, datetime
from nextcord.ext import commands
from typing import List
from typing import Optional

""" TicTacToe """
class TicTacToeButton(nextcord.ui.Button):
    def __init__(self, x: int, y: int):
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return 

        if view.current_player == view.X:
            if interaction.user != player1:
                await interaction.response.send_message("Its not your Turn!", ephemeral=True)
            else:
                self.style = nextcord.ButtonStyle.danger
                self.label = 'X'
                self.disabled = True
                view.board[self.y][self.x] = view.X
                view.current_player = view.O
                content = f"It is now {player2} turn"
        
        else:
            if interaction.user != player2:
                await interaction.response.send_message("Its not your Turn!", ephemeral=True)
            else:
                self.style = nextcord.ButtonStyle.success
                self.label = 'O'
                self.disabled = True
                view.board[self.y][self.x] = view.O
                view.current_player = view.X
                content = f"It is now {player1} turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'{player1} won!'
            elif winner == view.O:
                content = f'{player2} won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)    


class TicTacToe(nextcord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class Games(commands.Cog, description="Play some games."):
    
    COG_EMOJI = "🎮"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        """
        When a message is sent, process it as a guess.
        Then, process any commands in the message if it's not a guess.
        """
        ref = message.reference
        if not ref or not isinstance(ref.resolved, nextcord.Message):
                return False

        else:        
            pass

    @commands.command(name="tictactoe", description="Playing TicTacToe.....", aliases=['ttt'])
    async def tic(self, ctx: commands.Context, enemy: nextcord.Member):
        """Starts a tic-tac-toe game with yourself."""
        global player1
        global player2

        player1 = ctx.author
        player2 = enemy

        await ctx.send(f'Tic Tac Toe: {player1} goes first', view=TicTacToe())


def setup(bot):
    bot.add_cog(Games(bot))
