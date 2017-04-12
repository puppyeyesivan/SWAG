instrument = ['00001.SZA']
start_date = '-'  #initialize the starting date
end_date = '-'

def initialize(context):
context.set_commission (PerDollarr(0.0015)) # initialize trading fee
       
def handle_data(context, data):
    
    if context.trading_day_index < 20: # run after 20 trading days
        return
       
    sid = context.symbol(instruments[0])
    price = data.current(sid, 'price') # current price
    high_point = data.history(sid, 'price', 20, '1d').max() # 20-days highest 
    low_point = data.history(sid, 'price', 10, '1d').min() # 10-days lowest    
        
  # hold a position 
    cur_position = context.portfolio.positions[sid].amount  
               
   #Strategy
    if price >= high_point  and cur_position == 0 and data.can_trade(sid):  
        context.order_target_percent(sid, 1) 
   
    elif price <= low_point  and cur_position > 0 and data.can_trade(sid): 
        context.order_target_percent(sid, 0)
