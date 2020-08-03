def getAddress(i):
   switcher={
      'OBC':'1',
      'EPS':'2',
      'ADB':'3',
      'COMMS':'4',
      'ADCS':'5',
      'PROP':'6',
      'DEBUG':'7',
      'EGSE':'8',
      'HPI':'100'
      }
   return switcher.get(i,0)
