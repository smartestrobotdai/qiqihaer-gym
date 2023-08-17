import FreeCAD, Part, FemGui

GRID_X = 12
GRID_Y = 8
SPACING = 3000
HEIGHT = 2000

def create_2_layer_grid(doc, x_count, y_count, spacing=10, height_difference=10):
    lines = []
    red_color = (1.0, 0.0, 0.0)  # RGB for red

    def add_edge_to_doc(p1, p2, edge_name):
      edge = Part.makeLine(p1, p2)
      obj = doc.addObject("Part::Feature", edge_name)
      obj.Shape = edge
      obj.ViewObject.ShapeColor = red_color
      return edge

    # Upper grid
    for i in range(x_count):
      for j in range(y_count - 1):
        p1 = FreeCAD.Vector(i * spacing, j * spacing, 0)
        p2 = FreeCAD.Vector(i * spacing, (j + 1) * spacing, 0)
        edge_name = f"Edge_Upper_X{i}_Y{j}_to_Y{j+1}"
        lines.append(add_edge_to_doc(p1, p2, edge_name))
        
    for j in range(y_count):
      for i in range(x_count - 1):
        p1 = FreeCAD.Vector(i * spacing, j * spacing, 0)
        p2 = FreeCAD.Vector((i + 1) * spacing, j * spacing, 0)
        edge_name = f"Edge_Upper_Y{j}_X{i}_to_X{i+1}"
        lines.append(add_edge_to_doc(p1, p2, edge_name))
        

    # a ugly workaround to make sure a vertex is inserted at the 
    # lower right corner.
    p1 = FreeCAD.Vector((x_count-1) * spacing, 0, 0)
    p2 = FreeCAD.Vector((x_count-1) * spacing + 100, 0, 0)
    edge_name = "temp"
    lines.append(add_edge_to_doc(p1, p2, edge_name))


    # Lower grid
    for i in range(x_count - 1):
        for j in range(y_count - 2):
            p1 = FreeCAD.Vector((i + 0.5) * spacing, (j + 0.5) * spacing, -height_difference)
            p2 = FreeCAD.Vector((i + 0.5) * spacing, (j + 1.5) * spacing, -height_difference)
            edge_name = f"Edge_Lower_X{i}_Y{j}_to_Y{j+1}"
            lines.append(add_edge_to_doc(p1, p2, edge_name))
    for j in range(y_count - 1):
        for i in range(x_count - 2):
            p1 = FreeCAD.Vector((i + 0.5) * spacing, (j + 0.5) * spacing, -height_difference)
            p2 = FreeCAD.Vector((i + 1.5) * spacing, (j + 0.5) * spacing, -height_difference)
            edge_name = f"Edge_Lower_Y{j}_X{i}_to_X{i+1}"
            lines.append(add_edge_to_doc(p1, p2, edge_name))
            

    # Connectors
    for i in range(x_count - 1):
        for j in range(y_count - 1):
            lower_point = FreeCAD.Vector((i + 0.5) * spacing, (j + 0.5) * spacing, -height_difference)
            upper_points = [
                FreeCAD.Vector(i * spacing, j * spacing, 0),
                FreeCAD.Vector((i + 1) * spacing, j * spacing, 0),
                FreeCAD.Vector(i * spacing, (j + 1) * spacing, 0),
                FreeCAD.Vector((i + 1) * spacing, (j + 1) * spacing, 0)
            ]
            k = 1
            for up in upper_points:              
              edge_name = f"Edge_Connector_Y{j}_X{i}_{k}"
              lines.append(add_edge_to_doc(lower_point, up, edge_name))
              k+=1
              

    # Combine all lines into a single compound and add to the document
    grid = Part.makeCompound(lines)
    obj = doc.addObject("Part::Feature", "2LayerGrid")
    obj.Shape = grid
    obj.ViewObject.ShapeColor = red_color



# Get the active document
doc = FreeCAD.ActiveDocument

# Create the 2 layer grid with the provided parameters
create_2_layer_grid(doc, GRID_X, GRID_Y, SPACING, HEIGHT)

# start FEM
analysis = ObjectsFem.makeAnalysis(FreeCAD.ActiveDocument, 'Analysis')
FemGui.setActiveAnalysis(FreeCAD.ActiveDocument.ActiveObject)
ObjectsFem.makeSolverCalculixCcxTools(FreeCAD.ActiveDocument)
FemGui.getActiveAnalysis().addObject(FreeCAD.ActiveDocument.ActiveObject)


def add_fixed_constraint(doc, name, vertex_name="Vertex1"):
  fixed_constraint = doc.addObject("Fem::ConstraintFixed", name)
  fixed_constraint.Scale = 1
  fixed_constraint.References = [(doc.getObject(name), vertex_name)]
  FemGui.getActiveAnalysis().addObject(fixed_constraint)

for y in range(GRID_Y-1):
  edge_name = f'Edge_Upper_X{0}_Y{y}_to_Y{y+1}'
  add_fixed_constraint(doc, edge_name)
  edge_name = f'Edge_Upper_X{GRID_X-1}_Y{y}_to_Y{y+1}'
  add_fixed_constraint(doc, edge_name)

for x in range(1, GRID_X-1):
  edge_name = f'Edge_Upper_X{x}_Y{0}_to_Y{1}'
  add_fixed_constraint(doc, edge_name)
  edge_name = f'Edge_Upper_X{x}_Y{GRID_Y-2}_to_Y{GRID_Y-1}'
  add_fixed_constraint(doc, edge_name, vertex_name="Vertex2")
  



# stress is the stress in N/m^2
def get_total_force(stress, x_count, y_count, spacing_in_meter):
  # calculate the area
  print(x_count, y_count, spacing_in_meter)
  area = (x_count - 1) * (y_count - 1) * spacing_in_meter * spacing_in_meter
  print('area=', area)
  # calculate the force
  force = area * stress
  return force


def get_edges(x_start=0):
  edges = []

  def append_edge(edge_name):
    edges.append((doc.getObject(edge_name), 'Edge1'))

  for x in range(x_start, GRID_X):
    for y in range(GRID_Y):
      if y > 0:
        edge_name = f'Edge_Upper_X{x}_Y{y-1}_to_Y{y}'
        append_edge(edge_name)
      edge_name = f'Edge_Upper_Y{y}_X{x}_to_X{x+1}'
      append_edge(edge_name)
  
  return edges


def add_load(stress, x_start, load_name):
  load_edges = doc.addObject("Fem::ConstraintForce", load_name)
  load_edges.Force = get_total_force(stress, GRID_X-x_start, GRID_Y, SPACING/1000)
  load_edges.DirectionVector = FreeCAD.Vector(0,0,-1)
  edges = get_edges(x_start=x_start)
  load_edges.References = edges
  FemGui.getActiveAnalysis().addObject(load_edges)
  

# ceiling weight in N/m^2 (2400N/m^2)
# steel self weight in N/m^2 (260N/m^2)	

add_load(2400+260, 0, "ceilingSelfWeight")



# assume that the perlite package is 0.6*0.3*0.2 in size
# each pack is 20kg
# the height is 1.2m
# the weight is 20kg/(0.6*0.4*0.2)*1.2 = 500kg
add_load(5000, 8, "perliteWeight")


# snow + active load:1000
add_load(1000*1.35, 0, "snowActiveLoad")


doc.recompute()
