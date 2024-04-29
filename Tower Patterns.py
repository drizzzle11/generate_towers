import rhinoscriptsyntax as rs
import math

# Function for generating Pattern 1
def GenerateMod1(IMAX, JMAX, KMAX, Pattern, x, y, z):
    pi = math.pi
    imax = IMAX
    jmax = JMAX
    kmax = KMAX
    x1 = x
    y1 = y
    z1 = z
    pattern = Pattern
    point = {}
    midPt = []
    # Storing co-ordinates in a dictionary
    for i in range(imax):
        for j in range(jmax):
            for k in range(kmax):
                x = x1 + i * 16 + math.tan(i) * pi * pattern
                y = y1 + i * 16 + math.tan(j) * pi * pattern
                z = z1 + i * 16 + math.tan(k) * pi * pattern
                point[(i, j, k)] = (x, y, z)
    for i in range(imax):
        for j in range(jmax):
            for k in range(kmax):
                if i > 0 and j > 0 and k > 0:
                    midPt.append(MidPt(point[(i, j, k)], point[(i, j - 1, k)]))
                    midPt.append(MidPt(point[(i, j, k)], point[(i - 1, j, k)]))
                    midPt.append(MidPt(point[(i - 1, j, k)], point[(i - 1, j - 1, k)]))
                    midPt.append(MidPt(point[(i - 1, j - 1, k)], point[(i, j - 1, k)]))
                    midPt.append(MidPt(point[(i - 1, j - 1, k)], point[(i, j - 1, k - 1)]))
                    midPt.append(MidPt(point[(i - 1, j - 1, k - 1)], point[(i, j - 1, k - 1)]))
                    midPt.append(MidPt(point[(i, j - 1, k - 1)], point[(i, j - 1, k)]))
                    midPt.append(MidPt(point[(i, j - 1, k - 1)], point[(i, j, k - 1)]))
                    midPt.append(MidPt(point[(i, j, k)], point[(i, j, k - 1)]))
                    midPt.append(MidPt(point[(i, j, k - 1)], point[(i - 1, j, k - 1)]))
                    midPt.append(MidPt(point[(i - 1, j, k)], point[(i - 1, j, k - 1)]))
                    midPt.append(MidPt(point[(i - 1, j, k - 1)], point[(i - 1, j - 1, k - 1)]))

    t = GenerateSurfaces(midPt)
    return t
    
# Function to generate surfaces
def GenerateSurfaces(MidPoint):
    midPt = MidPoint
    srf = []
    for i in range(0, len(midPt)-11, 12):
        curve_1 = rs.AddCurve((midPt[i], midPt[i+ 1], midPt[i+2], midPt[i+3])) 
        curve_2 = rs.AddCurve((midPt[i+3], midPt[i+4], midPt[i+5], midPt[i+6])) 
        srf.append(rs.AddEdgeSrf((curve_1, curve_2)))
        rs.DeleteObjects(curve_1) 
        rs.DeleteObjects( curve_2) 
    return srf

# Function to Calculate the Midpoint
def MidPt(aP1, aP2):
    Midpt = None
    if aP1 is not None and aP2 is not None:
        Midpt = [0, 0, 0]
        for i  in range(3):
            Midpt[i] = (aP1[i] + aP2[i]) / 2
    return Midpt

def Main():
    # Take input values from the user to generate the geometric assembly
    imax = rs.GetInteger('max number of x points in module grid', 7)
    jmax = rs.GetInteger('max number of y points in module grid', 3)
    kmax = rs.GetInteger('max number of z points in module grid', 7)
    pattern = rs.GetInteger('pattern factor for module grid', 4)
    angle_rotation = rs.GetInteger('angle of rotation of the tower', 45)
    pi = math.pi
    Angle = 0.0
    x = 0
    y = 0
    rs.EnableRedraw(False)
#    Loop for making the overall tower that sends values to different functions to generate the modules first and then create the overall pattern
    for z in rs.frange(0.0, 13.0, 0.5):
        Angle = z * (pi / 2)  # Corrected Angle calculation
        for a in rs.frange(0.0, 2 * pi, (pi / 4)):
            x = 150 * math.sin(a + Angle)
            y = 150 * math.cos(a + Angle)
            rs.RotateObjects(GenerateMod1(imax, jmax, kmax, pattern, x, y, z), [0, 0, 0], angle_rotation * z)
    rs.EnableRedraw(True)

if __name__ == "__main__":
    Main()
