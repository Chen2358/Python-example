简易的密码和Email检测

面向AIP编程，即先设计API，再实现

@staticmethod:返回函数的静态方法，该方法不强制要求传递参数，类可以不用实例化就可以调用，也可以实例化后调用

class C(object):

  @staticmethod
  
  def f():
  
    pass
    
  
C.f()     #不用实例化调用

cobj = C()

cobj.f()  #实例化后调用

使用

import checkPwdandEmail

checkPwdandEmail.password('123')
