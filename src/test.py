import FreeCAD, Part

GRID_X = 19
GRID_Y = 14
SPACING = 2000
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

# Add fixed constraints.
fixed_constraint = doc.addObject("Fem::ConstraintFixed", "ConstraintFixed")
doc.ConstraintFixed.Scale = 1
doc.ConstraintFixed.References = [(App.ActiveDocument.Edge_Upper_X18_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X18_Y0_to_Y1,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y1_to_Y2,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y2_to_Y3,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y3_to_Y4,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y4_to_Y5,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y5_to_Y6,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y6_to_Y7,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y7_to_Y8,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y8_to_Y9,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y9_to_Y10,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y10_to_Y11,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y11_to_Y12,"Vertex2"), (App.ActiveDocument.Edge_Upper_X18_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X17_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X16_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X15_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X14_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X13_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X12_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X11_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X10_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X9_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X8_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X7_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X6_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X5_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X4_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X3_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X2_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X1_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y12_to_Y13,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y11_to_Y12,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y10_to_Y11,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y9_to_Y10,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y8_to_Y9,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y7_to_Y8,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y6_to_Y7,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y5_to_Y6,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y4_to_Y5,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y3_to_Y4,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y2_to_Y3,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y1_to_Y2,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y0_to_Y1,"Vertex2"), (App.ActiveDocument.Edge_Upper_X0_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X1_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X2_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X3_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X4_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X5_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X6_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X7_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X8_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X9_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X10_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X11_Y0_to_Y1,"Vertex1"), (App.ActiveDocument._LayerGrid,"Vertex313"), (App.ActiveDocument.Edge_Upper_X13_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X14_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X15_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X16_Y0_to_Y1,"Vertex1"), (App.ActiveDocument.Edge_Upper_X17_Y0_to_Y1,"Vertex1")]
FemGui.getActiveAnalysis().addObject(fixed_constraint)

# Force calculation:
# every grid's area: 2000*2000 = 4 m^2
# the ceiling weight: 2.4KN/m^2
# steel structure weight: 0.26KN/m^2
# total force: (2.4+0.26)*4 = 10.64
# force on edges on the middle:
# 10.64/2 = 5320N
self_weight_middle_edges = doc.addObject("Fem::ConstraintForce", "selfWeightMiddle")
self_weight_middle_edges.Force = 5320
self_weight_middle_edges.DirectionVector = FreeCAD.Vector(0,0,-1)

# force on edges on the border: 
# 10.64/4=2660N
self_weight_border_edges = doc.addObject("Fem::ConstraintForce", "selfWeightBorder")
self_weight_border_edges.Force = 2660
self_weight_border_edges.DirectionVector = FreeCAD.Vector(0,0,-1)

middle_edges = []
border_edges = []
for x in range(GRID_X-1):
  for y in range(GRID_Y-1):
    if x == 0 or x == GRID_X - 2 or y == 0 or y == GRID_Y - 2:
      edges = border_edges
    else:
      edges = middle_edges
    edge1_name = f'Edge_Upper_X{x}_Y{y}_to_Y{y+1}'
    edge2_name = f'Edge_Upper_Y{y}_X{x}_to_X{x+1}'
    edges.append((doc.getObject(edge1_name),"Edge1"))
    edges.append((doc.getObject(edge2_name),"Edge1"))

doc.selfWeightMiddle.References = middle_edges
FemGui.getActiveAnalysis().addObject(self_weight_middle_edges)


doc.selfWeightBorder.References = border_edges
FemGui.getActiveAnalysis().addObject(self_weight_border_edges)


# the perlite weight: 3.0KN/m^2
# total force on square: 3*4 = 12KN
# force on the middle edges: 12/2 = 6KN

perlite_force_middle_edges = doc.addObject("Fem::ConstraintForce", "perliteForceMiddle")
perlite_force_middle_edges.Force = 6000
perlite_force_middle_edges.DirectionVector = FreeCAD.Vector(0,0,-1)

# force on the border edges: 12/4 = 3kN
perlite_force_border_edges = doc.addObject("Fem::ConstraintForce", "perliteForceBorder")
perlite_force_border_edges.Force = 3000
perlite_force_border_edges.DirectionVector = FreeCAD.Vector(0,0,-1)

perlite_middle_edges = []
perlite_border_edges = []
for x in range(14, GRID_X-1):
  for y in range(GRID_Y-1):
    if x == 14 or x == GRID_X - 2 or y == 0 or y == GRID_Y - 2:
      edges = perlite_border_edges
    else:
      edges = perlite_middle_edges
    edge1_name = f'Edge_Upper_X{x}_Y{y}_to_Y{y+1}'
    edge2_name = f'Edge_Upper_Y{y}_X{x}_to_X{x+1}'
    edges.append((doc.getObject(edge1_name),"Edge1"))
    edges.append((doc.getObject(edge2_name),"Edge1"))

doc.perliteForceMiddle.References = perlite_middle_edges
FemGui.getActiveAnalysis().addObject(perlite_force_middle_edges)


doc.perliteForceBorder.References = perlite_border_edges
FemGui.getActiveAnalysis().addObject(perlite_force_border_edges)


doc.recompute()
