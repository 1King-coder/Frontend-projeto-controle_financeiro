from .colors import colors

class btn_style:
    
    small = {
        'height': 40,
        'width': 80,
        'font': ('Roboto', 18),
        'corner_radius': 10,
        'fg_color': colors['color2'],
        'border_width': 2,
        'border_color': colors['color4'],
        'text_color': colors['color5']

    }

    medium = {
        'height': 60,
        'width': 160,
        'font': ('Roboto', 18),
        'corner_radius': 10,
        'fg_color': colors['color2'],
        'border_width': 2,
        'border_color': colors['color4'],
        'text_color': colors['color5']
    }

    large = {
        'height': 80,
        'width': 200,
        'font': ('Roboto', 18),
        'corner_radius': 10,
        'fg_color': colors['color2'],
        'border_width': 2,
        'border_color': colors['color5'],
        'text_color': colors['color5']
    }

class lbl_style:

    light_rectangle_bg = {
        'small': {
            'font': ('Roboto', 14),
            'corner_radius': 4,
            'fg_color': colors['color2'],    
            'text_color': colors['color5'],
            
        },
        'medium': {
            'font': ('Roboto', 16),
            'corner_radius': 4,
            'fg_color': colors['color2'],    
            'text_color': colors['color5'],
        },
        'large': {
            'font': ('Roboto', 18),
            'corner_radius': 4,
            'fg_color': colors['color2'],    
            'text_color': colors['color5'],
            
        },
        'entry_lbl': {
            'font': ('Roboto', 14),
            'corner_radius': 4,
            'fg_color': colors['color2'],    
            'text_color': colors['color5'],
            'padx': 1,
            'pady': 4
        }
    }

    dark_rectangle_bg = {
        'small': {
            'font': ('Roboto', 14),
            'corner_radius': 4,
            'fg_color': colors['color1'],    
            'text_color': colors['color5'],
            
        },
        'medium': {
            'font': ('Roboto', 16),
            'corner_radius': 4,
            'fg_color': colors['color1'],    
            'text_color': colors['color5'],
        },
        'large': {
            'font': ('Roboto', 18),
            'corner_radius': 4,
            'fg_color': colors['color1'],    
            'text_color': colors['color5'],
            
        },
        'entry_lbl': {
            'font': ('Roboto', 14),
            'corner_radius': 4,
            'fg_color': colors['color1'],    
            'text_color': colors['color5'],
            'padx': 1,
            'pady': 4
        }
    }

class frame_style:
    fg_1 = {
        'fg_color': colors['color1'],
        'corner_radius': 4
    }

    fg_2 = {
        'fg_color': colors['color2'],
        'corner_radius': 4
    }

    fg_3 = {
        'fg_color': colors['color3'],
        'corner_radius': 4
    }


class progressbar_style:
    small = {
        'fg_color': colors['color2'],
        'border_width': 2,
        'border_color': colors['color4'],
        'corner_radius': 10,
        'height': 20
    }

    medium = {
        'fg_color': colors['color2'],
        'border_width': 4,
        'border_color': colors['color4'],
        'corner_radius': 16,
        'height': 40
    }

    large = {
        'fg_color': colors['color2'],
        'border_width': 8,
        'border_color': colors['color5'],
        'corner_radius': 20,
        'height': 60
    }


class scale_style:
    small = {
        'fg_color': colors['color2'],
        'border_width': 2,
        'border_color': colors['color4'],
        'corner_radius': 10,
        'length': 120,
        'sliderlength': 40
    }

    medium = {
        'fg_color': colors['color2'],
        'border_width': 4,
        'border_color': colors['color4'],
        'corner_radius': 16,
        'length': 160,
        'sliderlength': 60
    }

    large = {
        'fg_color': colors['color2'],
        'border_width': 8,
        'border_color': colors['color5'],
        'corner_radius': 20,
        'length': 200,
        'sliderlength': 80
    }


class radio_style:
    small = {
        'font': ('Roboto', 14),
        'fg_color': colors['color2'],
        'border_width': 2,
        'border_color': colors['color4'],
        'corner_radius': 10,
        'text_color': colors['color5']
    }

    medium = {
        'font': ('Roboto', 16),
        'fg_color': colors['color2'],
        'border_width': 4,
        'border_color': colors['color4'],
        'corner_radius': 16,
        'text_color': colors['color5']
    }

    large = {
        'font': ('Roboto', 18),
        'fg_color': colors['color2'],
        'border_width': 8,
        'border_color': colors['color5'],
        'corner_radius': 20,
        'text_color': colors['color5']
    }


class checkbox_style:
    small = {
        'font': ('Roboto', 14),
        'fg_color': colors['color2'],
        'border_width': 2,
        'border_color': colors['color4'],
        'corner_radius': 10,
        'text_color': colors['color5']
    }

    medium = {
        'font': ('Roboto', 16),
        'fg_color': colors['color2'],
        'border_width': 4,
        'border_color': colors['color4'],
        'corner_radius': 16,
        'text_color': colors['color5']
    }

    large = {
        'font': ('Roboto', 18),
        'fg_color': colors['color2'],
        'border_width': 8,
        'border_color': colors['color5'],
        'corner_radius': 20,
        'text_color': colors['color5']
    }

class entry_style:
    small = {
        'font': ('Roboto', 14),
        'fg_color': colors['color1'],
        'corner_radius': 4,
        'text_color': colors['color5'],
        'width': 150,
        'height': 40
    }

    medium = {
        'font': ('Roboto', 16),
        'fg_color': colors['color1'],
        'corner_radius': 4,
        'text_color': colors['color5'],
        'width': 200,
        'height': 50
    }

    large = {
        'font': ('Roboto', 18),
        'fg_color': colors['color1'],
        'corner_radius': 4,
        'text_color': colors['color5'],
        'width': 300,
        'height': 60
    }  

class textbox_style:
    small = {
        'font': ('Roboto', 14),
        'width': 200,
        'height': 100,
        'fg_color': colors['color3'],
        'corner_radius': 4,
        'text_color': colors['color5']
    }

    medium = {
        'font': ('Roboto', 16),
        'width': 200,
        'height': 100,
        'fg_color': colors['color3'],
        'corner_radius': 4,
        'text_color': colors['color5']
    }

    large = {
        'font': ('Roboto', 18),
        'width': 200,
        'height': 100,
        'fg_color': colors['color3'],
        'corner_radius': 4,
        'text_color': colors['color5']
    }

class combobox_style:
    default = {
        'fg_color': colors['color1'],
        'corner_radius': 4,
        'font': ('Roboto', 14),
        'dropdown_font': ('Roboto', 14),
        'text_color': colors['color5']
    }


class switch_style:
    default = {
        'bg_color': colors['color1'],
        'border_color': colors['color5'],
        'width': 40,
        'height': 20,
        'switch_width': 40,
        'switch_height': 20,
        'border_width': 2,
        'corner_radius': 10,
        'font': ('Roboto', 20),
        'text_color': colors['color5']

    }



