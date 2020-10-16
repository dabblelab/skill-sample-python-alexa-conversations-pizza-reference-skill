""" 
Copyright 2020 Amazon.com, Inc. and its affiliates. All Rights Reserved.
SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0

Licensed under the Amazon Software License (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

http://aws.amazon.com/asl/

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""

daily_specials = {
  "sunday" : {
    "lunch" : {
      "pizza" : {
        "size": "small", 
        "crust": "thin crust",
        "cheese" : "extra", 
        "toppings_list" : ["pineapple", "canadian bacon"]
      },
      "salad" : "small caesar salad",
      "drinks" : "large iced tea",
      'cost' : 10.99
    },
    "dinner" : {
      "pizza" : {
        "size": "extra large", 
        "crust": "deep dish",
        "cheese" : "normal", 
        "toppings_list" : ["ham", "pepperoni", "sausage", "black olives"]
      },
      "salad" : "large house salad",
      "drinks" : "2 liter coke",
      "side" : "cheesy garlic bread",
      "dessert" : "two homemade chocolate fudge cookies",
      "cost" : 21.99
    }
  },
  "monday" : {
    "lunch" : {
      "pizza" : {
        "size": "small", 
        "crust": "regular",
        "cheese" : "extra", 
        "toppings_list" : ["pepperoni", "olives"]
      },
      "salad" : "small house salad",
      "drinks" : "diet coke",
      "cost" : 10.99
    },
    "dinner" : {
      "pizza" : {
        "size": "large", 
        "crust": "regular",
        "cheese" : "extra", 
        "toppings_list" : ["kalamata olives", "artichoke hearts", "feta cheese"]
      },
      "salad" : "large caesar salad",
      "drinks": "2 liter sprite",
      "side": "parmesean bread bites",
      "dessert": "a family size fudge brownie",
      "cost" : 14.99
    }
  },
  "tuesday" : {
    "lunch" : {
      "pizza" : {
        "size": "medium", 
        "crust": "brooklyn style",
        "cheese" : "regular", 
        "toppingsList" : ["pepperoni"]
      },
      "salad" : "small caesar salad",
      "drinks" : "sprite",
      "cost" : 11.99
    },
    "dinner" : {
      "pizza" : {
        "size": "extra large", 
        "crust": "brooklyn style",
        "cheese" : "normal", 
        "toppings_list" : ["tomato", "basil", "ricotta cheese"]
      },
      "salad" : "small house salad",
      "drinks": "one liter San Pelligrino",
      "dessert": "chocolate dipped strawberries",
      "side": "basil garlic toast",
      "cost" : 14.99
    }
  },
  "wednesday" : {
    "lunch" : {
      "pizza" : {
        "size": "small", 
        "crust": "thin",
        "cheese" : "normal", 
        "toppings_list" : ["parmesean flakes", "olive oil"]
      },
      "salad" : "small caesar salad",
      "drinks" : "large iced tea",
      "cost" : 10.99
    },
    "dinner" : {
      "pizza" : {
        "size": "large", 
        "crust": "thin",
        "cheese" : "light", 
        "toppings_list" : ["chicken", "spinach", "mushroom"]
      },
      "salad" : "large caesar salad",
      "drinks" : "2 liter diet coke",
      "dessert" : "a box of pocky sticks",
      "side" : "garlic bread sticks",
      "cost" : 19.99
    }
  },
  "thursday" : {
    "lunch" : {
      "pizza" : {
        "size": "small", 
        "crust": "regular",
        "cheese" : "extra", 
        "toppings_list" : ["bacon", "canadian bacon", "sausage"]
      },
      "salad" : "small house salad",
      "drinks" : "diet coke",
      "cost" : 9.99
    },
    "dinner" : {
      "pizza" : {
        "size": "extra large", 
        "crust": "regular",
        "cheese" : "light", 
        "toppings_list" : ["tomato", "onion", "garlic"]
      },
      "salad" : "small house salad",
      "side": "olive tapenade and fresh sliced bread",
      "drinks": "a two liter sprite",
      "dessert" : "small apple pie",
      "cost" : 18.99
    }
  },
  "friday" : {
    "lunch" : {
      "pizza" : {
        "size": "medium", 
        "crust": "regular",
        "cheese" : "light", 
        "toppings_list" : ["sausage", "onion", "sweet peppers"]
      },
      "salad" : "small caesar salad",
      "drinks": "iced tea",
      "cost" : 10.99
    },
    "dinner" : {
      "pizza" : {
        "size": "extra large", 
        "crust": "deep dish",
        "cheese" : "normal", 
        "toppings_list" : ["ham", "pepperoni", "sausage", "black olives"]
      },
      "salad" : "large house salad",
      "drinks" : "2 liter coke",
      "side" : "ranch cheesy bites with dipping sauce",
      "dessert" : "a truffle brownie",
      "cost" : 22.99
    }
  },
  "saturday" : {
    "lunch" : {
      "pizza" : {
        "size": "small", 
        "crust": "brooklyn style",
        "cheese" : "extra", 
        "toppings_list" : ["tomato", "basil"]
      },
      "salad" : "small house salad",
      "drinks" : "large iced tea",
      "cost" : 10.99
    },
    "dinner" : {
      "pizza" : {
        "size": "extra large", 
        "crust": "thin",
        "cheese" : "normal", 
        "toppings_list" : ["pineapple", "canadian bacon"]
      },
      "salad" : "large house salad",
      "drinks": "two, two liter cokes",
      "dessert": "homemade raspberry pie",
      "side" : "ranch cheesy bites with dipping sauce",
      "cost" : 18.99
    }
  },
}

specials = [
  { 
    "name" : "three cheese delight", 
    "qty": 1, 
    "pizza": { 
      "size": "large", 
      "crust": "deep dish",
      "cheese" : "extra", 
      "toppings_list" : ["asiago", "mozzarella blend", "ricotta"]
    },
    "cost": 12.99
  },
  { 
    "name" : "pepperoni party", 
    "qty": 1, 
    "pizza" : {
      "size": "extra large",
      "crust": "regular",
      "cheese" : "extra", 
      "toppings_list" : ["old world dry aged pepperoni", "molinari pepperoni", "pepper crusted pepperoni", "fresh basil", "roasted ricotta medallions"]
    },
    "cost": 10.99
  },
  {
    "name" : "meat lovers", 
    "qty": 1, 
    "pizza" : {
      "size": "large",
      "crust": "regular",
      "cheese" : "light", 
      "toppings_list" : ['sausage', 'pepperoni', 'ham', 'bacon']
    },
    "cost": 9.99
  },
  {
    "name" : "veggie supreme", 
    "qty": 1, 
    "pizza": {
      "size": "large",
      "crust": "thin",
      "cheese" : "normal", 
      "toppings_list": ["spinach", "olives", "mushrooms", "onions", "artichoke hearts"]
    },
    "cost": 8.99
  },
  {
    "name" : "kitchen sink", 
    "qty": 1, 
    "pizza": {
      "size": "extra large",
      "crust": "deep dish",
      "cheese" : "extra", 
      "toppings_list": ["ham", "bacon", "pepperoni", "sausage", "onions", "black olives", "green peppers", "jalapenos", "feta cheese"]
    },
    "cost": 13.99
  },
  {
    "name" : "two medium, two topping pizzas", 
    "qty": 2, 
    "pizza": {
      "size": "medium",
      "crust": "regular",
      "cheese": "normal", 
      "toppingsList": ["your choice of two toppings"]
    },
    "cost": 10.99
}]

pizza_costs = {
  "small": 5.99,
  "medium": 7.99,
  "large": 10.99,
  "extra large" : 13.99
}

feeding_size = {
  "small" : "around one adult",
  "medium" : "around two adults",
  "large" : "between two and three adults",
  "extra large" : "three to four adults"
}

salad_costs = {
  "small" : 4.99,
  "large" : 7.99,
  "custom" : 6.99
}

salads = [
  "small house salad",
  "large house salad",
  "small caesar salad",
  "large caesar salad"
]

sides = [
  {"name": "garlic bread sticks", "cost": 4.99},
  {"name": "ranch cheesy bites with dipping sauce", "cost": 5.99},
  {"name": "cheesy garlic bread", "cost": 5.99}
]

desserts = [
  {"name": "truffle brownie", "cost": 1},
  {"name": "small apple pie", "cost": 3.99},
  {"name": "homemade chocolate fudge cookies", "cost": 1.50}
]

drinks = [
  {"name": "iced tea", "cost": 1.99},
  {"name": "lemonade", "cost": 1.99},
  {"name": "sprite", "cost": 1.99},
  {"name": "water", "cost": 1.99},
  {"name": "pepsi", "cost": 1.99},
  {"name": "diet coke", "cost": 1.99},
  {"name": "coke", "cost": 1.99},
  {"name": "two liter coke", "cost": 3.99},
  {"name": "two liter diet coke", "cost": 3.99},
  {"name": "two liter sprite", "cost": 3.99},
  {"name": "two liter pepsi", "cost": 3.99}
]

def generate_order_text(order):
  order_text = ""
  cost = 0

  if order.get('special', False) is True:
    order_text = "a {special_name} comes with {qty} {size}".format(order['special']['name'], order['special']['qty'], order['special']['pizza']['size'])
    speakable_toppings = order['special']['pizza']['toppings_list']
    last_topping = speakable_toppings.pop()
    order_text += "{speakable_toppings} {last_topping} pizza".format(", ".join(speakable_toppings), last_topping)
    order_text += " on {crust} with {cheese} ".format(order["special"]["pizza"]["crust"], order["special"]["pizza"]["cheese"])
    if order["special"]["cost"] is not None:
      cost += order["special"]["cost"]

  if order.get("pizza", None) is not None:
    print("pizza IS {}".format(order["pizza"]))
    print("type of pizza IS {}".format(type(order["pizza"])))
    print("inside {}".format(order["pizza"].get("size", None)))
    
    order_text += " a {size}".format(order["pizza"]["size"])
    speakable_toppings = order["pizza"]["toppingsList"]
    last_topping = "and {}".format(speakable_toppings.pop())
    order_text += "{speakable_toppings} {last_topping} pizza".format(", ".join(speakable_toppings), last_topping)
    order_text += " on {crust} with {cheese} ".format(order["pizza"]["crust"], order["pizza"]["cheese"])
    cost += get_pizza_cost(order["pizza"]["size"])

  if order.get("salad", None) is not None:
    if order_text is not None:
      order_text += ", "
    
    order_text += "a {}".format(order["salad"])
    cost += get_salad_cost(order["salad"])

  if order.get("drinks", None) is not None:
    if order_text is not None:
      order_text += ", "

    if order.get("side", None) is None and order.get("dessert", None) is None:
      order_text += " and "

    order_text += "a {}".format(order["drinks"])
    cost += get_drink_cost(order["drinks"])
  
  if order.get("side", None) is not None:
    if order_text is not None:
      order_text += ", "

    if order.get("dessert", None) is None:
      order_text += " and "

    order_text += "a side order of {}".format(order["side"])
    cost += get_side_cost(order["side"])

  if order.get("dessert", None) is not None:
    if order_text is not None:
      order_text += ", "

    order_text += "{}".format(order["dessert"])
    cost += get_dessert_cost(order["dessert"])
  
  order_text += " for a total of ${}".format(cost)
  return order_text

def get_daily_special_for_period(day, period):
  return daily_specials[day][period]

def get_pizza_reference_specials():
  def map_func(special):
    return special['name']
  return map(map_func, specials)

def get_special_pizza_details(pizza_name):
  print("In getSpecialPizzaDetails, looking for: {}".format(pizza_name))
  if pizza_name not in get_pizza_reference_specials():
    return None
  for special in specials:
    if special['name'].lower() or pizza_name in special['name'].lower():
      return special
  return None

def get_pizza_cost(size):
  return pizza_costs[size]

def get_salad_cost(salad):
  cost = 0
  for type in ["small", "large", "custom"]:
    if type in salad:
      cost = salad_costs[type]
  return cost

def get_special_cost(name):
  for special in specials:
    if special["name"] == name:
      return special["cost"]  

def get_salads():
  def salads_func(salad):
    return salad["name"]
  return map(salads_func, salads)

def get_drinks():
  def drinks_func(drink):
    return drink["name"]
  return map(drinks_func, drinks)

def get_drink_cost(drink):
  # silly since all drinks cost $1.99 but this give you the chance to alter the menu 
  # and not affect the logic
  for _drink in drinks:
    if _drink["name"] == drink:
      return _drink["cost"]

def get_sides():
  def sides_func(side):
    return side["name"]
  return map(sides_func, sides)

def get_side_cost(side):
  for _side in sides:
    if _side["name"] == side:
      return _side["cost"]

def get_desserts():
  def desserts_func(dessert):
    return dessert["name"]
  return map(desserts_func, desserts)

def get_dessert_cost(dessert):
  for _dessert in desserts:
    if _dessert["name"] == dessert:
      return _dessert["cost"]

def make_speakable_list(list):
  if len(list) > 1:
    last = " and " + list.pop();
    return ", ".join(list) + last
  return list

def get_feeding_size(size):
  return feeding_size[size]
