# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 19:37:51 2016

@author: Joe
"""

import os, sys
import xml.etree.ElementTree as ET

# parse slicer xml string and generate Voreen transfer functions
def parse_slicer_xml(tffilename, scalar, color):
    xa=[float(i) for i in scalar.split()]
    xrgb=[float(i) for i in color.split()]
    n1=int(xa[0]/2)
    n2=int(xrgb[0]/4)
    n=min(n1,n2)
    if n1!=n2:
        print("scalarOpacity's size does not match colorTransfer's size, the smaller size is used.", n1, n2)
    
    list_intensity = []
    list_split = []
    list_r = []
    list_g = []
    list_b = []
    list_a = []
    
    for i in range(n):
    #    print i,xa[2*i+1],xa[2*i+2]
        x=xa[2*i+1]
        a=xa[2*i+2]
    #    x=xrgb[4*i+1]
        r=xrgb[4*i+2]
        g=xrgb[4*i+3]
        b=xrgb[4*i+4]
        
        if x>=0 and x<=255:
        	# add a control point at 0
            if x>0 and len(list_intensity)<1:
                list_intensity.append(0)
                list_split.append("false")
                list_r.append(r)
                list_g.append(g)
                list_b.append(b)
                list_a.append(a)
                
            list_intensity.append(x)
            list_split.append("false")
            list_r.append(r)
            list_g.append(g)
            list_b.append(b)
            list_a.append(a)
            
        # add a control point at 255
        elif x>255:
            if len(list_intensity) > 0:
                r0=list_r[-1]
                g0=list_g[-1]
                b0=list_b[-1]
                a0=list_a[-1]
            else:
                r0=r
                g0=g
                b0=b
                a0=a

            list_intensity.append(255)
            list_split.append("false")
            list_r.append(r0)
            list_g.append(g0)
            list_b.append(b0)
            list_a.append(a0)
            break;
    
    domain_x='0'
    domain_y='1'
    threshold_x='0'
    threshold_y='1'
    
    # build XML tree
    root1 = ET.Element("VoreenData")
    root1.set("version", "1")
    TransFuncIntensity1 = ET.SubElement(root1, "TransFuncIntensity")
    TransFuncIntensity1.set("type", "TransFuncIntensity")
    domain1 = ET.SubElement(TransFuncIntensity1, "domain")
    domain1.set("x", domain_x)
    domain1.set("y", domain_y)
    threshold1 = ET.SubElement(TransFuncIntensity1, "threshold")
    threshold1.set("x", threshold_x)
    threshold1.set("y", threshold_y)
    Keys1 = ET.SubElement(TransFuncIntensity1, "Keys")
    
    # fill x, r, g, b, a values into XML elements
    for i in range(len(list_intensity)):
        key1 = ET.SubElement(Keys1, "key")
        key1.set("type", "TransFuncMappingKey")
        intensity1 = ET.SubElement(key1, "intensity")
        intensity1.set("value", str(list_intensity[i]/255))
        split1 = ET.SubElement(key1, "split")
        split1.set("value", list_split[i])
        colorL1 = ET.SubElement(key1, "colorL")
        colorL1.set("r", str(int(list_r[i]*255+1e-3)))
        colorL1.set("g", str(int(list_g[i]*255+1e-3)))
        colorL1.set("b", str(int(list_b[i]*255+1e-3)))
        colorL1.set("a", str(int(list_a[i]*255+1e-3)))
    
    # write XML element tree to file
    xml_string = ET.tostring(root1)
    import xml.dom.minidom as MD
    xml =  MD.parseString(xml_string)
    pretty_xml_as_string = xml.toprettyxml()
    root2 = ET.fromstring(pretty_xml_as_string)
    et2 = ET.ElementTree(root2)
    et2.write(tffilename, encoding='utf-8', xml_declaration=True)

if __name__ == "__main__":
    print(sys.argv[0], os.path.sep)
    # read filename from command line arguments
    if len(sys.argv)>=2:
        filename = sys.argv[-1]
    else:
        filename = os.path.join(os.path.dirname(sys.argv[0]), "presets.xml")

    tree = ET.parse(filename)
    root = tree.getroot()
    path=os.path.dirname(filename)
    
    for child in root:
        name=child.get("name")
        scalar=child.get("scalarOpacity")
        color=child.get("colorTransfer")
        tffilename=os.path.join(path, name+".tfi")
        print(name, tffilename)
        parse_slicer_xml(tffilename, scalar, color)
