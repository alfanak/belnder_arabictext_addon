bl_info = {
    "name": "Write Arabic Text",
    "author": "رشيد محي الدين",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "Text Data > Arabic text",
    "description": "Write Arabic text",
    "warning": "",
    "wiki_url": "",
    "category": "Text",
}

import bpy

class panel_arabictext(bpy.types.Panel):

    bl_label = "Arabic text"
    bl_idname = "main"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    
    @classmethod 
    def poll(cls, context):
        if bpy.context.scene.objects.active.type == 'FONT':
            return True
        return False
    
    def draw(self, context):
        
        
        layout = self.layout

        scene = context.scene

        layout.label(text="Write text down:")

        row = layout.row()
        row.operator("object.btn_addtext")
        sub_row = row.row()
        sub_row.scale_x = 3.0
        sub_row.prop(context.scene, "arabic_text")
        
class btn_addtext(bpy.types.Operator):
    
    bl_label = "Insert Text"
    bl_idname = "object.btn_addtext"
    bl_description = "Insert text"
    
    def execute(self, context):
        
        arabic_text().apply_text()
        
        return {'FINISHED'}

class arabic_text():
    
    # TODO:
    # find a way to update text in the input box (if its possible)
    
    # Arabic chars
    
    arabic_chars = ['ا', 'أ', 'إ', 'آ', 'ء', 'ب', 'ت', 'ث', 'ج',
                    'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص',
                    'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل',
                    'م', 'ن', 'ه', 'ة','و', 'ؤ', 'ي', 'ى', 'ئ']
                    
    right_connectable_chars = ['ا', 'أ', 'إ', 'آ', 'ب', 'ت', 'ث', 'ج', 'ح',
                               'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض',
                               'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م',
                               'ن', 'ه', 'ة','و', 'ؤ', 'ي', 'ى', 'ئ']
                               
    left_connectable_chars = ['ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'س', 'ش', 'ص',
                              'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل',
                              'م', 'ن', 'ه', 'ي', 'ى', 'ئ']
    
    #                          ا       أ       إ       آ       ء       ب       ت       ث       ج
    chars_variants_bases = [0xFE8D, 0xFE83, 0xFE87, 0xFE81, 0xFE80, 0xFE8F, 0xFE95, 0xFE99, 0xFE9D,
    #                          ح       خ       د       ذ       ر       ز       س       ش       ص 
                            0xFEA1, 0xFEA5, 0xFEA9, 0xFEAB, 0xFEAD, 0xFEAF, 0xFEB1, 0xFEB5, 0xFEB9, 
    #                          ض       ط       ظ       ع       غ       ف       ق       ك       ل
                            0xFEBD, 0xFEC1, 0xFEC1, 0xFEC9, 0xFECD, 0xFED1, 0xFED5, 0xFED9, 0xFEDD,
    #                          م       ن       ه       ة       و       ؤ       ي       ى       ئ
                            0xFEE1, 0xFEE5, 0xFEE9, 0xFE93, 0xFEED, 0xFE85, 0xFEF1, 0xFEEF, 0xFE89]
    
    # is_right_connectable
    
    def is_right_connectable(c):
        if c in arabic_text.right_connectable_chars:
            return True
        return False
    
    # is_left_connectable
    
    def is_left_connectable(c):
        if c in arabic_text.left_connectable_chars:
            return True
        return False        
    
    # get_char_index
    
    def get_char_index(c):

        if c not in arabic_text.arabic_chars: # not an arabic char
            return -1
        
        return arabic_text.arabic_chars.index(c)
    
    # get_char_variants_base
    
    def get_char_variants_base(c):
        
        char_index = arabic_text.get_char_index(c)
        
        if char_index == -1: # not an arabic char
            return -1
        
        return arabic_text.chars_variants_bases[char_index]
    
    # generate text
    
    def generate_text():
        
        original_string = bpy.context.scene.arabic_text
        
        new_string = []
        
        previous_char = ""
        next_char = ""
        
        char_code = 0
        
        char_counter = 0
        
        skip_char = False
        
        for current_char in original_string:
            
            if skip_char:
                skip_char = False
                continue
            
            # reset variables
            previous_char = ""
            next_char = ""

            #
            
            if char_counter > 0:
                previous_char = original_string[char_counter - 1]
                
            if char_counter < len(original_string) - 1:
                next_char = original_string[char_counter +1]
            
            # Lem-Alef
            
            if current_char == 'ل':
                
                if next_char == 'ا':
                    char_code = 0xFEFB
                elif next_char == 'أ':
                    char_code = 0xFEF7
                elif next_char == 'إ':
                    char_code = 0xFEF9
                elif next_char == 'آ':
                    char_code = 0xFEF5
                else:
                    char_code = 0
                
                if char_code != 0:
                    if self.is_left_connectable(previous_char):
                        char_code += 1
                    new_string.insert(0, chr(char_code))
                    
                    char_counter += 2
                    skip_char = True
                    continue
            
            # other letters
            
            char_code = arabic_text.get_char_variants_base(current_char);
            
            if char_code == -1: # current_char is not an arabic char (not found in arabic_chars[])
                new_string.insert(0, current_char)
                char_counter += 1
                continue
            
            # its an arabic char
            
            if arabic_text.is_left_connectable(previous_char) and arabic_text.is_right_connectable(current_char):
                if arabic_text.is_left_connectable(current_char) and arabic_text.is_right_connectable(next_char):
                    char_code += 3
                else:
                    char_code += 1
            else:
                if arabic_text.is_left_connectable(current_char) and arabic_text.is_right_connectable(next_char):
                    char_code += 2
                    
            new_string.insert(0, chr(char_code)) # put chars in reverse order
            
            char_counter += 1
            
        text =''.join(new_string)
        
        return text

    # apply text

    def apply_text(scene):
        
        text = arabic_text.generate_text()
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.font.delete()
        bpy.ops.font.text_insert(text = text)
        bpy.ops.object.editmode_toggle()    

# register

def register():

    def update(self, context):
        
        arabic_text().apply_text()
        
        return
    
    bpy.types.Scene.arabic_text = bpy.props.StringProperty \
      (
        name = "",
        description = "كتابة نص باللغة العربية",
        default = "نص",
        update = update
      )

    bpy.utils.register_module(__name__)

# unregsiter

def unregister():
    
    del bpy.types.Scene.arabic_text
    
    bpy.utils.unregister_module(__name__)

