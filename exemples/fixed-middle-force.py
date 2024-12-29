from uvatool import Node, Apoio, NodalForce, Element, Process, Print, Structure

"""
____    ____  __    _______      ___      
\   \  /   / |  |  /  _____|    /   \     
 \   \/   /  |  | |  |  __     /  ^  \    
  \      /   |  | |  | |_ |   /  /_\  \   
   \    /    |  | |  |__| |  /  _____  \  
    \__/     |__|  \______| /__/     \__\ 

 _______ .__   __.   _______      ___           _______..___________.     ___       _______       ___      
|   ____||  \ |  |  /  _____|    /   \         /       ||           |    /   \     |       \     /   \     
|  |__   |   \|  | |  |  __     /  ^  \       |   (----``---|  |----`   /  ^  \    |  .--.  |   /  ^  \    
|   __|  |  . `  | |  | |_ |   /  /_\  \       \   \        |  |       /  /_\  \   |  |  |  |  /  /_\  \   
|  |____ |  |\   | |  |__| |  /  _____  \  .----)   |       |  |      /  _____  \  |  '--'  | /  _____  \  
|_______||__| \__|  \______| /__/     \__\ |_______/        |__|     /__/     \__\ |_______/ /__/     \__\ 
"""

n1 = Node(0, 0)
n2 = Node(2.5, 0)
n3 = Node(5, 0)

n1.setSupport(Apoio.terceiro_genero)
n2.setNodalForce(NodalForce(0, -20, 0))

e1 = Element(n1, n2, 1, 1, 1)
e2 = Element(n2, n3, 1, 1, 1)

nodes = [n1, n2, n3]
elements = [e1, e2]


if __name__ == "__main__":
    calc = Process(nodes, elements)

    results = Print(calc)
    results.nodalDisplacement()
else:
    structure = Structure("EXEMPLO DE UTILIZAÇÃO", nodes, elements)
