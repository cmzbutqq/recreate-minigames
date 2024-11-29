// A practice of functional programming && recursion
#include <iostream>
#include <array>
#include <tuple>
#include <vector>
#include <algorithm>
using namespace std;

enum chess_t
{
    none,
    black,
    white,
    tied
};
using row_t = array<chess_t, 3>;
using board_t = array<row_t, 3>;

board_t emptyBoard({{{none, none, none}, {none, none, none}, {none, none, none}}});

board_t replace(int i, int j, chess_t val, const board_t &b)
{
    board_t newBoard(b);
    newBoard[i][j] = val;
    return newBoard;
}

chess_t winner(const board_t &board)
{
    for (int i : {0, 1, 2})
    {
        if (board[i][0] == board[i][1] and board[i][0] == board[i][2] and board[i][0] != none)
            return board[i][0];
        if (board[0][i] == board[1][i] and board[0][i] == board[2][i] and board[0][i] != none)
            return board[0][i];
    }
    if (board[0][0] == board[1][1] and board[0][0] == board[2][2] and board[0][0] != none)
        return board[0][0];
    if (board[0][2] == board[1][1] and board[0][2] == board[2][0] and board[0][2] != none)
        return board[0][2];
    for (int i : {0, 1, 2})
        for (int j : {0, 1, 2})
            if (board[i][j] == none)
                return none;
    return tied;
}

int value(const board_t &board, chess_t player)
{
    chess_t status = winner(board);
    if (status == black)
        return 1;
    if (status == white)
        return -1;
    if (status == tied)
        return 0;
    chess_t opponent = (player == black) ? white : black;
    vector<pair<int, board_t>> nexts = {};
    for (int i : {0, 1, 2})
    {
        for (int j : {0, 1, 2})
        {
            if (board[i][j] == none)
            {
                board_t new_board(replace(i, j, player, board));
                nexts.push_back(make_pair(value(new_board, opponent), new_board));
            }
        }
    }
    auto comp = [](const pair<int, board_t> &a, const pair<int, board_t> &b)
    { return a.first < b.first; };
    if (player == black)
        return max_element(nexts.begin(), nexts.end(), comp)->first;
    else
        return min_element(nexts.begin(), nexts.end(), comp)->first;
}

board_t best_next(const board_t &board, chess_t player)
{
    chess_t opponent = (player == black) ? white : black;
    vector<pair<int, board_t>> nexts = {};
    for (int i : {0, 1, 2})
    {
        for (int j : {0, 1, 2})
        {
            if (board[i][j] == none)
            {
                board_t new_board(replace(i, j, player, board));
                nexts.push_back(make_pair(value(new_board, opponent), new_board));
            }
        }
    }
    auto comp = [](const pair<int, board_t> &a, const pair<int, board_t> &b)
    { return a.first < b.first; };
    if (player == black)
        return max_element(nexts.begin(), nexts.end(), comp)->second;
    else
        return min_element(nexts.begin(), nexts.end(), comp)->second;
}

void print(const board_t &board)
{
    for (int i : {0, 1, 2})
    {
        for (int j : {0, 1, 2})
        {
            switch (board[i][j])
            {
            case none:
                cout << ' ';
                break;
            case black:
                cout << 'B';
                break;
            case white:
                cout << 'W';
                break;
            }
            cout << ' ';
        }
        cout << '\n';
    }
}
int main()
{
    board_t current(emptyBoard);
    chess_t player = black;
    chess_t ai = (player == black) ? white : black;
    int i, j;
    bool ai_help = 1;

    if (ai_help)
    {
        while (winner(current) == none)
        {
            current = best_next(current, player);
            cout << "Player places.\n";
            print(current);
            if (winner(current) != none)
                goto announce;
            cout << "AI placed.\n";
            current = best_next(current, ai);
            print(current);
            if (winner(current) != none)
                goto announce;
            cout << "Your turn.\n";
        }
    }
    else
    {
        while (winner(current) == none)
        {
            do
                cin >> i >> j;
            while (current[i][j] != none);
            current = replace(i, j, player, current);
            cout << "Player places at " << i << " " << j << ".\n";
            print(current);
            if (winner(current) != none)
                goto announce;
            cout << "AI placed.\n";
            current = best_next(current, ai);
            print(current);
            if (winner(current) != none)
                goto announce;
            cout << "Your turn.\n";
        }
    }
announce:
    if (winner(current) == player)
        cout << "You win.\n";
    else if (winner(current) == ai)
        cout << "You lose.\n";
    else
        cout << "Draw.\n";

    return 0;
}