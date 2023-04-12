"""Renders all variations"""
import os
from os.path import exists
import bpy

DIAS_LIST = [('', "color.png"),('sinus_a_2', "image1.png"), ('sinus_a_6', "image2.png"), ('sinus_a_12', "image3.png")]
print(DIAS_LIST)
_DEBUG = False

class RenderList(bpy.types.Operator):
    bl_idname = "render.list"
    bl_label = "Render Analog List"

    cancel_render = None
    rendering = None
    render_queue = None
    timer_event = None
    total = 0
    
    #LOGOS_PATH = "//logos"
    OUTPUT_PATH = "//results"
    
    def render_init(self, scene, depsgraph):
        self.rendering = True
        print("RENDER INIT", self.make_filename(self.render_queue[0]))

    def render_complete(self, scene, depsgraph):
        self.render_queue.pop(0)
        self.rendering = False

    def render_cancel(self, scene, depsgraph):
        self.cancel_render = True
        print("RENDER CANCEL")

    def exists(self, render_filename):
        output_path = self.OUTPUT_PATH + os.sep + render_filename + ".png"
        return exists(output_path)

    def make_filename(self, qitem):
        #if (qitem["faucet_color"] is None):
        #    faucet_color = ""
        #else:
        #    faucet_color = "-" + qitem["faucet_color"]["label"]
        #return  bpy.path.clean_name( os.sep + "_cam-" + qitem["camera"].lower())
        path = qitem["output"]
        #print("x",qitem["output"], path)
        return path
    
    def remove_dias(self):
        for obj in bpy.data.collections['Dias'].objects:
            obj.hide_render = True
           
    def make_dias_list(self, folder):
        for d,f in DIAS_LIST:
            if _DEBUG:
                print ("Adding to list",d,f)
            self.render_queue.append({"dias": d, "output": f})
        
        #self.render_queue.append({"dias": "gitter_a_2", "output":"gitter_a_2.png" })
        #self.render_queue.append({"dias": "gitter_a_6", "output":"gitter_a_6.png" })
        #self.render_queue.append({"dias": "gitter_a_12", "output":"gitter_a_12.png" })
        
        self.total = len(self.render_queue)
 
        if _DEBUG:
            print("Make List - Total: " + str(self.total))
            print(self.render_queue)
        
    def execute(self, context):
        print('starting execute')
        self.cancel_render = False
        self.rendering = False
        self.render_queue = []
        

        TOPS = ["none", "Top1", "Top2", "Top3"]

        LEFTS = ["none", "Left1", "Left2", "Left3"]

        FAUCETS = ["none", "Faucet"]

        GAUGES = ["none", "Gauge"]

        FAUCET_COLORS   = [
            {"color": (1, 0, 0, 1), "label": "red"},
            {"color": (0.985, 0.621, 0, 1), "label": "yellow"},
            {"color": (0.05, 0.05, 0.05, 1), "label": "black"}
        ]

        # Determine cameras
        #cam_collection = bpy.data.collections['Cameras']
        #CAMERAS = [{"name": str(i), "value": o.name}
        #           for i, o in enumerate(cam_collection.objects)]
                   
        
# --- Build render queue -----------------------------------------------------

        #logodir = bpy.path.abspath(self.LOGOS_PATH)
        
        #for file_path in os.listdir( logodir ): 
        #    if (file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg') or file_path.lower().endswith('.png')):
        #        logo = {"name": os.path.splitext(file_path)[0], "path": logodir + os.sep + file_path}
        #        
        #        for cam in CAMERAS:
        #            for top in TOPS:
        #                for left in LEFTS:
        #                    for gauge in GAUGES:
        #                        for faucet in FAUCETS:
        #                            if (faucet == "none"):
        #                                self.render_queue.append({
        #                                    "logo": logo,
        #                                    "camera": cam["value"],
        #                                    "top": top,
        #                                    "left": left,
        #                                    "gauge": gauge,
        #                                    "faucet": faucet,
        #                                    "faucet_color": None,
        #                                })
        #                            else:
        #                                for faucet_color in FAUCET_COLORS:
        #                                    self.render_queue.append({
        #                                        "logo": logo,
        #                                        "camera": cam["value"],
        #                                        "top": top,
        #                                        "left": left,
        #                                        "gauge": gauge,
        ##                                        "faucet": faucet,
        #                                        "faucet_color": faucet_color,
        #                                    })
        
        self.make_dias_list('')
        
        #self.render_queue.append({"logo": "ddD", "camera": "Camera", "output":"ud1.png"     })
        #self.render_queue.append({"logo": "ddD1", "camera": "Camera", "output":"ud2.png"    })
        #self.render_queue.append({"logo": "ddD2", "camera": "Camera",  "output":"ud3.png"    })
        
        self.total = len(self.render_queue)
        print("Render Queue Total: " + str(self.total))
        #print(self.render_queue)
        
# ----------------------------------------------------------------------------

        # Register callback functions
        bpy.app.handlers.render_init.clear()
        bpy.app.handlers.render_init.append(self.render_init)

        bpy.app.handlers.render_complete.clear()
        bpy.app.handlers.render_complete.append(self.render_complete)

        bpy.app.handlers.render_cancel.clear()
        bpy.app.handlers.render_cancel.append(self.render_cancel)

        # Lock interface
        bpy.types.RenderSettings.use_lock_interface = True
        
        # Create timer event that runs every second to check if render render_queue needs to be updated
        self.timer_event = context.window_manager.event_timer_add(0.5, window=context.window)
        
        # register this as running in background
        context.window_manager.modal_handler_add(self)
        
        print ("Execute END")
        return {"RUNNING_MODAL"}
        
    def modal(self, context, event):
        #print("starting modal", context, event)
        # ESC
        if event.type == 'ESC':
            bpy.types.RenderSettings.use_lock_interface = False
            print("CANCELLED")
            return {'CANCELLED'}

        # timer event every second
        elif event.type == 'TIMER':
            # If cancelled or no items in queue to render, finish.
            if len(self.render_queue) == 0 or self.cancel_render is True:

                # remove all render callbacks
                bpy.app.handlers.render_init.clear()
                bpy.app.handlers.render_complete.clear()
                bpy.app.handlers.render_cancel.clear()
                
                # remove timer
                context.window_manager.event_timer_remove(self.timer_event)
                
                bpy.types.RenderSettings.use_lock_interface = False

                print("FINISHED")
                return {"FINISHED"}

            elif self.rendering is False:
                # nothing is rendering and there are items in queue
                
                sc = bpy.context.scene
                qitem = self.render_queue[0]

                render_filename = self.make_filename(qitem)
                print("-Start new Render", render_filename)
                #print("render filename", render_filename)
                
                output_path = self.OUTPUT_PATH + os.sep + render_filename
                #print("Output path", output_path)
                
                # Skip if file exists
                if exists(bpy.path.abspath(output_path)):
                    self.render_queue.pop(0)
                    print("Skipping " + render_filename + ", queue length: " + str(len(self.render_queue)))
                else:
                    print("Rendering " + str(self.total + 1 - len(self.render_queue)
                                             ) + "/" + str(self.total) + ": " + render_filename)
                   
                    self.remove_dias()
                    dias = bpy.data.collections['Dias'].objects
                    print("dias", dias)
                    if qitem['dias'] in dias:
                        print("Selecting qitem", qitem)
                        obj = dias[qitem['dias']]
                        #print(obj)
                        obj.hide_render = False
                    else:
                        print("Dias ", qitem['dias'], "does not exist")

                
                    # defaults
                    #for obj in bpy.data.collections['Base'].objects:
                    #    obj.hide_render = False
                    #for obj in bpy.data.collections['Tops'].objects:
                    #    obj.hide_render = False
                    #for obj in bpy.data.collections['Lefts'].objects:
                    #    obj.hide_render = False
                        

                    # Top
                    #for obj in bpy.data.collections['Tops'].objects:
                    #    obj.hide_render = obj.name != qitem["top"]

                    # Left
                    #for obj in bpy.data.collections['Lefts'].objects:
                    #    obj.hide_render = obj.name != qitem["left"]
                        
                    # Faucet 
                    #bpy.data.collections['Base'].objects["Faucet"].hide_render = qitem["faucet"] != "Faucet"
                    
                    # Faucet color
                    #if (qitem["faucet"] != "none"):
                    #    mat = bpy.data.materials["Faucet"]
                    #    principled = mat.node_tree.nodes["Principled BSDF"]
                    #    principled.inputs["Base Color"].default_value = qitem["faucet_color"]["color"]                       
                    
                    # Gauge 
                    #bpy.data.collections['Base'].objects["Gauge"].hide_render = qitem["gauge"] != "Gauge"
                        
                    # Logo
                    #mat = bpy.data.materials["Logo"]
                    #principled = mat.node_tree.nodes["Principled BSDF"]
                    #texture = principled.inputs["Base Color"].links[0].from_node
                    #if (texture):
                    #    texture.image = bpy.data.images.load(qitem["logo"]["path"])

                    # Change scene active camera
                    #cameraName = qitem["camera"]
                    #if cameraName in sc.objects:
                    #    sc.camera = bpy.data.objects[cameraName]
                    #else:
                    #    self.report(
                    #        {'ERROR_INVALID_INPUT'}, message="Can not find camera "+cameraName+" in scene!")
                    #    return {'CANCELLED'}
                    
                    cameraName = 'Camera'
                    sc.render.filepath = output_path

                    bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)
                        
                
        return {"PASS_THROUGH"}
                

def register():
    bpy.utils.register_class(RenderList)

def unregister():
    bpy.utils.unregister_class(RenderList)
    
if __name__ == "__main__":
    print("------------------ START ----------------------")
    register()
    obj_list = ['fil1.stl', 'fil2.stl']
    print("Object List", obj_list)
    bpy.ops.render.list()