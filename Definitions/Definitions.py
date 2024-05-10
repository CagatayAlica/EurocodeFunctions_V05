import Section.Materials as mat
import Section.CreateSections as sec
import Section.GrossSectionProp as gr
import Main as man

inp = man.userInputs()
steel = mat.material(inp.MatName, inp.fy, inp.fu)
section = sec.LippedCSection(inp.A, inp.B, inp.C, inp.t, inp.R)
gross = gr.GrossProperties(section.x, section.y, section.thk, section.thk)

