from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def Registration_menu(*args):
    keyboard = VkKeyboard(inline=True)

    keyboard.add_button(label= "112", color=VkKeyboardColor.POSITIVE, payload={"command": "reg_class", "argument": "112"})
    keyboard.add_button(label= "122", color=VkKeyboardColor.POSITIVE, payload={"command": "reg_class", "argument": "122"})
    keyboard.add_button(label= "132", color=VkKeyboardColor.POSITIVE, payload={"command": "reg_class", "argument": "132"})
    keyboard.add_button(label= "142", color=VkKeyboardColor.POSITIVE, payload={"command": "reg_class", "argument": "142"})
    keyboard.add_button(label= "152", color=VkKeyboardColor.POSITIVE, payload={"command": "reg_class", "argument": "152"})

    return keyboard.get_keyboard()