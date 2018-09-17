1、状态机

state 存储当前状态， state_actions 这个词典变量作为状态转换的规则，它的 key 是状态，value 是返回下一个状态的函数：

Init: init()
  Game
  
Game: game()
  Game
  Win
  GameOver
  Exit
  
Win: lambda: not_game('Win')
  Init
  Exit
  
Gameover: lambda: not_game('Gameover')
  Init
  Exit
  
Exit: 退出循环
状态机会不断循环，直到达到 Exit 终结状态结束程序。
