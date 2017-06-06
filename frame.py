import os

import pygame as pg


class MultiPanelFrame(object):
    def __init__(self, rects, image_directory):
    
        self.frame_images = self.get_frame_images(image_directory)
        self.cell_size = self.frame_images["vert"].get_width()
        grid = {} 
        neighbor_grid = {}
        if len(rects) > 1:
            outside_rect = rects[0].unionall(rects[1:])
        else:
             outside_rect = rects[0]        
        for x in range(outside_rect.left, outside_rect.right, self.cell_size):
            for y in range(outside_rect.top, outside_rect.bottom, self.cell_size):
                grid[(x, y)] = None
                neighbor_grid[(x, y)] = ""
        self.outside_rect = outside_rect
        print "OUT: {}".format(self.outside_rect)
        self.panels = []
        self.frame_single_rect(outside_rect, grid)
        for rect in rects:
            print rect
            self.frame_single_rect(rect, grid)
            self.panels.append(pg.Rect(rect))     
        for cell_index in grid.keys():
            self.calc_neighbors(cell_index, grid, self.cell_size, neighbor_grid)
        self.frame_pieces = self.assign_pieces(grid, neighbor_grid)    
            
    def get_frame_images(self, img_directory):
        images = {}
        names = ["vert", "tl corner", "tee left", "cross"]
        img_names = ["frame-vertical", "frame-tl-corner", "frame-tee-left", "frame-cross"]
        print os.listdir(img_directory)
        for name, img_name in zip(names, img_names):
            images[name] = pg.image.load(os.path.join(img_directory, "{}.png".format(img_name)))
        images["horiz"] = pg.transform.rotate(images["vert"], 90)
        images["tee right"] = pg.transform.flip(images["tee left"], True, False)
        images["tee down"] = pg.transform.rotate(images["tee left"], 90)
        images["tee up"] = pg.transform.flip(images["tee down"], False, True)
        images["tr corner"] = pg.transform.flip(images["tl corner"], True, False)
        images["bl corner"] = pg.transform.flip(images["tl corner"], False, True)
        images["br corner"] = pg.transform.flip(images["tr corner"], False, True)
        return images
        
    def frame_single_rect(self, rect, grid):
        w, h = rect.topleft
        for x in range(rect.left, rect.right, self.cell_size):
            grid[(x, rect.top)] = True
            grid[(x, rect.bottom - self.cell_size)] = True
        for y in range(rect.top, rect.bottom, self.cell_size):
            grid[(rect.left, y)] = True
            grid[(rect.right - self.cell_size, y)] = True

    def calc_neighbors(self, cell_index, grid, cell_size, neighbor_grid):
        cx, cy = cell_index
        for offset, direction in zip(((-1, 0), (1, 0), (0, -1), (0, 1)), ("w", "e", "n", "s")):
            x, y = cell_size * offset[0], cell_size * offset[1]
            try:
                if grid[(cx + x, cy + y)]:
                    neighbor_grid[cell_index] += direction
            except KeyError:
                pass
                
    def assign_pieces(self, grid, neighbor_grid):
        direction_map = {
            "we": "horiz",
            "wen": "tee up",
            "wens": "cross",
            "wes": "tee down",
            "wn": "br corner",
            "wns": "tee left",
            "ws": "tr corner",
            "en": "bl corner",
            "ens": "tee right",
            "es": "tl corner",
            "ns": "vert"}
        pieces = []
        outside_left, outside_top = self.outside_rect.topleft
        for cell_index in neighbor_grid.keys():
            if grid[cell_index]:
                img_name = direction_map[neighbor_grid[cell_index]]
                img = self.frame_images[img_name]
                rect = img.get_rect(topleft=cell_index)
                pieces.append((img, rect))
        return pieces
    
    def draw(self, surface):
        for img, rect in self.frame_pieces:
            surface.blit(img, rect)  
        #for p in self.panels:
        #    pg.draw.rect(surface, pg.Color("red"), p, 1)

        
            
            