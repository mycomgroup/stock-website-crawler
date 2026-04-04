import sys
try:
    import jqresearch
    print("jqresearch modules:")
    print(dir(jqresearch))
except Exception as e:
    print(e)
    
try:
    from jqresearch import api
    print("jqresearch.api modules:")
    print(dir(api))
except Exception as e:
    print(e)
    
try:
    import kuanke
    print("kuanke modules:")
    print(dir(kuanke))
except Exception as e:
    print(e)
    
try:
    from kuanke.user_space import api
    print("kuanke.user_space.api modules:")
    print([x for x in dir(api) if not x.startswith('_')])
except Exception as e:
    print(e)
