from compass.testcase import TestCase
from compass.validate import compare_variables
from compass.ocean.tests.hurricane.mesh.dequ120at30cr10rr2 \
    import DEQU120at30cr10rr2Mesh


class Mesh(TestCase):
    """
    A test case for creating a global MPAS-Ocean mesh

    Attributes
    ----------
    mesh_step : compass.ocean.tests.hurricane.mesh.mesh.MeshStep
        The step for creating the mesh
    """
    def __init__(self, test_group, mesh_name):
        """
        Create test case for creating a global MPAS-Ocean mesh

        Parameters
        ----------
        test_group : compass.ocean.tests.global_ocean.GlobalOcean
            The global ocean test group that this test case belongs to

        mesh_name : str
            The name of the mesh
        """
        self.mesh_name = mesh_name
        name = 'mesh'
        subdir = '{}/{}'.format(mesh_name, name)
        super().__init__(test_group=test_group, name=name, subdir=subdir)
        if mesh_name == 'DEQU120at30cr10rr2':
            self.mesh_step = DEQU120at30cr10rr2Mesh(
                                 self, mesh_name,
                                 preserve_floodplain=False)
        if mesh_name == 'DEQU120at30cr10rr2WD':
            self.mesh_step = DEQU120at30cr10rr2Mesh(
                                 self, mesh_name,
                                 preserve_floodplain=True)
        self.add_step(self.mesh_step)

        self.with_ice_shelf_cavities = False

    def configure(self):
        """
        Modify the configuration options for this test case
        """
        self.config.add_from_package(self.mesh_step.package,
                                     self.mesh_step.mesh_config_filename,
                                     exception=True)

    def run(self):
        """
        Run each step of the testcase
        """
        step = self.mesh_step
        config = self.config
        # get the these properties from the config options
        step.cores = config.getint('global_ocean', 'mesh_cores')
        step.min_cores = config.getint('global_ocean', 'mesh_min_cores')

        # run the step
        super().run()

    def validate(self):
        """
        Test cases can override this method to perform validation of variables
        and timers
        """
        variables = ['xCell', 'yCell', 'zCell']
        compare_variables(test_case=self, variables=variables,
                          filename1='mesh/culled_mesh.nc')
