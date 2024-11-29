/*
planned:
    

unplanned:
    linux support
    colored_terminal
    multithread
    GUI
    key bind settings , tick time & fps settings(useless)
*/

#include <iostream>
#include <vector>
#include <random>
#include <unistd.h>  //for sleep,usleep
#include <chrono>    //for timer
#include <conio.h>   //for keydetect
#include <Windows.h> //for double buffering
using namespace std::chrono;
using namespace std;

HANDLE hOutput = GetStdHandle(STD_OUTPUT_HANDLE);
COORD coord = {0, 0};

enum State
{
    welcome_state,
    game_state,
    dead_state,
    option_state
} state;

enum direction
{
    up,
    down,
    left,
    right,
    none
};

struct GlobalStatus
{
    int length = 5;
    int height = 5;
    bool haveWall = false;
    char palette[5] = {'$', '#', '.', 'O', '+'};
    int keybinds[5] = {119, 115, 97, 100, 0};

    const int framerate = 60, frametime = 1e3 / framerate, // ms
        ticktime = 0.5e3;                                    // ms

} global_status;

struct GameContainer
{
    vector<vector<int>> playground;
    bool dead = false;
    int snake_len = 0;
    direction dir = none;
    int key = 0;

    GameContainer();
    void draw_map();
    void set_bonus();
    void step();
    void debug_dir();
};

long long int get_time();
void state_controller();
void welcome_screen();
void option_screen();
void game_screen();
void death_screen();

int main()
{
    state = welcome_state;
    state_controller();
    return 0;
}

void state_controller()
{
    while (true)
    {
        switch (state)
        {
        case welcome_state:
            welcome_screen();
            break;
        case game_state:
            game_screen();
            break;
        case dead_state:
            death_screen();
            break;
        case option_state:
            option_screen();
            break;
        default:
            throw runtime_error("Unknown state");
            break;
        }
    }
}

void welcome_screen()
{
    cout << "Welcome to the game\n";
    usleep(0.5e6);
    cout << "Can only run on Windows with C++ 11 or later versions\n";
    usleep(0.5e6);
    cout << "MADE BY CMZ" << endl;
    usleep(1.5e6);
    srand((unsigned)time(NULL));
    state = option_state;
    return;
}

long long int get_time()
{
    return duration_cast<milliseconds>(high_resolution_clock::now().time_since_epoch()).count();
}

void option_screen()
{
    system("cls");
    auto print_option = []()
    { cout << "current settings:\nlength:" << global_status.length << "\theight:" << global_status.height << "\t wall:" << (global_status.haveWall ? "YES" : "NO") << endl; };
    auto print_keybinds = []()
    { cout << "current keybinds:\n(up,down,left,right)= "
           << global_status.keybinds[0] << ' ' << global_status.keybinds[1] << ' ' << global_status.keybinds[2] << ' ' << global_status.keybinds[3] << endl; };

    print_option();
settings:
    cout << "\n0:start\t1:change world settings\n";
    int choice;
    cin >> choice;
    switch (choice)
    {
    case 0:
        state = game_state;
        break;
    case 1:
        cout << "new length:";
        cin >> global_status.length;
        cout << "new height:";
        cin >> global_status.height;
        cout << "wall(y/n):";
        char y_or_n;
        cin >> y_or_n;
        if (y_or_n == 'y')
            global_status.haveWall = true;
        if (y_or_n == 'n')
            global_status.haveWall = false;
        cout<<endl;
        print_option();
        goto settings;
        break;
    default:
        state = game_state;
    }
    return;
}

void death_screen()
{
    system("cls");
    cout << "you died" << endl;
    cout << "1:restart\t2:options\t3:quit" << endl;
    int choice;
    cin >> choice;
    switch (choice)
    {
    case 1:
        state = game_state;
        break;
    case 2:
        state = option_state;
        break;
    case 3:
        cout << "bye" << endl;
        usleep(0.5e6);
        exit(0);
        break;
    default:
        state = welcome_state;
        break;
    }
    return;
}

void game_screen()
{
    // countdown
    usleep(0.5e6);
    cout << "\n3\n";
    usleep(0.5e6);
    cout << "2\n";
    usleep(0.5e6);
    cout << "1\n";
    usleep(0.5e6);
    cout << "start" << endl;
    // gen
    GameContainer game_instance;
    auto last_tick = get_time();
    auto last_frame = get_time();
    system("cls");
    // main loop
    while (true)
    {
        // set timer
        auto timer = get_time();
        // observe keyboard
        if (_kbhit())
        {
            game_instance.key = _getch();
            for (int i = 0; i < 4; i++)
            {
                if (game_instance.key == global_status.keybinds[i])
                    game_instance.dir = direction(i);
            }
            // cout<<game_instance.key<<endl;game_instance.debug_dir();//for keybind debug
        }
        // tick
        if (timer - last_tick >= global_status.ticktime)
        {
            last_tick = timer;
            // if dead
            if (game_instance.dead)
            {
                state = dead_state;
                return;
            }
            // alive
            game_instance.step();
        }
        // draw
        if (timer - last_frame >= global_status.frametime)
        {
            SetConsoleCursorPosition(hOutput, coord);
            last_frame = timer;
            cout << "score:" << game_instance.snake_len << endl;
            game_instance.draw_map();
        }
    }
    return;
}

GameContainer::GameContainer()
{
    // resize
    int length = global_status.length;
    int height = global_status.height;
    playground.resize(height);
    for (int i = 0; i < height; i++)
        playground[i].resize(length);
    // fill with blank: 0
    for (auto row : playground)
    {
        for (auto dot : row)
        {
            dot = 0;
        }
    }
    // set wall: -1
    if (global_status.haveWall)
    {
        for (int i = 0; i < height; i++)
        {
            playground[i][0] = -1;
            playground[i][length - 1] = -1;
        }
        for (int i = 0; i < length; i++)
        {
            playground[0][i] = -1;
            playground[height - 1][i] = -1;
        }
    }
    // head: 1 body: 2,3,4...
    auto gen_player = [this]()
    {
        int x = rand() % max((global_status.length - 2), 1) + 1;
        int y = rand() % max((global_status.height - 2), 1) + 1;
        this->playground[y][x] = 1;
        snake_len++;
    };
    gen_player();
    // set first bonus: -2
    set_bonus();
}

void GameContainer::set_bonus()
{
    vector<vector<int>> blank = {};
    for (int row = 0; row < global_status.height; row++)
    {
        for (int col = 0; col < global_status.length; col++)
        {
            if (!playground[row][col])
                blank.push_back({row, col});
        }
    }
    int rand_num = rand() % blank.size();
    playground[blank[rand_num][0]][blank[rand_num][1]] = -2;
}

void GameContainer::step()
{
    // get head tail & gen next_head
    int now_head[2], tail[2];
    int next_head[2];
    for (int row = 0; row < global_status.height; row++)
    {
        for (int col = 0; col < global_status.length; col++)
        {
            if (playground[row][col] == snake_len)
            {
                tail[0] = row;
                tail[1] = col;
            }
            if (playground[row][col] == 1)
            {
                now_head[0] = row;
                now_head[1] = col;

                switch (dir)
                {
                case direction::up:
                    next_head[0] = now_head[0] - 1;
                    next_head[1] = now_head[1];
                    break;
                case direction::down:
                    next_head[0] = now_head[0] + 1;
                    next_head[1] = now_head[1];
                    break;
                case direction::left:
                    next_head[0] = now_head[0];
                    next_head[1] = now_head[1] - 1;
                    break;
                case direction::right:
                    next_head[0] = now_head[0];
                    next_head[1] = now_head[1] + 1;
                    break;
                case none:
                    return; // no input no move()
                default:
                    throw runtime_error("Unknown direction");
                }
                next_head[0] += global_status.height;
                next_head[1] += global_status.length;
                next_head[0] %= global_status.height;
                next_head[1] %= global_status.length;
            }
        }
    }
    // check dead and act
    int next_head_val = playground[next_head[0]][next_head[1]];
    if (next_head_val != 0 && next_head_val != -2)
    {
        dead = true;
        return;
    }
    // check bonus
    bool on_bonus = false;
    if (next_head_val == -2)
    {
        on_bonus = true;
        snake_len++;
    }
    // age
    for (int row = 0; row < global_status.height; row++)
    {
        for (int col = 0; col < global_status.length; col++)
        {
            if (playground[row][col] > 0)
            {
                playground[row][col]++;
            }
        }
    }
    // gen head
    playground[next_head[0]][next_head[1]] = 1;
    // cut tail or gen bonus
    if (!on_bonus)
        playground[tail[0]][tail[1]] = 0;
    else
        set_bonus();
}

void GameContainer::draw_map()
{
    for (auto row : playground)
    {
        for (auto dot : row)
        {
            // draw blank wall bonus(0,-1,-2)
            if (dot <= 0)
                cout << global_status.palette[dot + 2] << " ";
            // draw snake head(1)
            else if (dot == 1)
                cout << global_status.palette[4] << " ";
            // draw snake body(2,3...)
            else
                cout << global_status.palette[3] << " ";
        }
        cout << '\n';
    }
}

void GameContainer::debug_dir()
{ // FOR DEBUG
    switch (dir)
    {
    case direction::up:
        cout << "up" << endl;
        break;
    case direction::down:
        cout << "down" << endl;
        break;
    case direction::left:
        cout << "left" << endl;
        break;
    case direction::right:
        cout << "right" << endl;
        break;
    default:
        break;
    }
}