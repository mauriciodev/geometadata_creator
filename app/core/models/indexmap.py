from django.db import models
from core.grid_utm import grid_utm


# class that implements table behavior to IndexMap.objects
class IndexMapManager(models.Manager):
    def __init__(self):
        super().__init__()
        self.grid_utm = None #object that computes inom

    def get_mi(self,inomen:str): 
        parts = inomen.split('-')
        sufix=''
      
        if len(parts) > 4: #1000000
            scale_denominator=100000
            if len(parts)>5: #50k or more
                sufix = '-'+'-'.join(parts[5:])
                inomen= '-'.join(parts[:5])
        elif len(parts) == 4:
            scale_denominator = 250000
        else:
            return ""
        rows = IndexMap.objects.filter(
            scale_denominator=scale_denominator, inomen=inomen
        )

        if len(rows) > 0:
            return f"{rows[0].mi}{sufix}"
        return ""

    def get_inomen_by_mi(self, mi: str, is_mir=False):
        parts = mi.split("-")
        sufix = ""

        if is_mir:
            scale_denominator = 250000
        else:
            scale_denominator = 100000

        if len(parts) > 1:  # 50k or more
            sufix = "-" + "-".join(parts[1:])

        rows = IndexMap.objects.filter(scale_denominator=scale_denominator, mi=parts[0])

        if len(rows) > 0:
            return f"{rows[0].inomen}{sufix}"
        return ""

    def get_grid_utm(self):  # returns the object
        if self.grid_utm is None:
            self.grid_utm = grid_utm()
        return self.grid_utm

    def get_inomen_from_extent(self, xmin, ymin, xmax, ymax):
        grid = self.get_grid_utm()
        return grid.inomenFromExtent(xmin, ymin, xmax, ymax)

    def get_inomen_from_rasterio(self, filepath):
        grid = self.get_grid_utm()
        return grid.getInomenFromRasterio(filepath)

    def get_inomen_mi_from_rasterio(self, filepath):
        inomen = self.get_inomen_from_rasterio(filepath)
        mi = self.get_mi(inomen)
        return (inomen, mi)


class IndexMap(models.Model):
    scale_denominator = models.IntegerField()
    mi = models.CharField(max_length=10)
    inomen = models.CharField(max_length=20)
    objects = IndexMapManager()

    def __str__(self):
        return f"{self.mi} - {self.inomen} ({self.scale_denominator})"
