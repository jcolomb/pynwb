from .core import NWBContainerMapper
from .. import register_map

from ..base import TimeSeries, ProcessingModule
from ..form.build import LinkBuilder


@register_map(ProcessingModule)
class ModuleMap(NWBContainerMapper):

    def __init__(self, spec):
        super(ModuleMap, self).__init__(spec)
        containers_spec = self.spec.get_neurodata_type('NWBDataInterface')
        self.map_spec('data_interfaces', containers_spec)

    @NWBContainerMapper.constructor_arg('name')
    def name(self, builder, manager):
        return builder.name


@register_map(TimeSeries)
class TimeSeriesMap(NWBContainerMapper):

    def __init__(self, spec):
        super(TimeSeriesMap, self).__init__(spec)
        data_spec = self.spec.get_dataset('data')
        self.map_attr('unit', data_spec.get_attribute('unit'))
        self.map_const_arg('unit', data_spec.get_attribute('unit'))
        self.map_attr('resolution', data_spec.get_attribute('resolution'))
        self.map_attr('conversion', data_spec.get_attribute('conversion'))
        timestamps_spec = self.spec.get_dataset('timestamps')
        self.map_attr('timestamps_unit', timestamps_spec.get_attribute('unit'))
        # self.map_attr('interval', timestamps_spec.get_attribute('interval'))
        startingtime_spec = self.spec.get_dataset('starting_time')
        self.map_attr('starting_time_unit', startingtime_spec.get_attribute('unit'))
        self.map_attr('rate', startingtime_spec.get_attribute('rate'))

    @NWBContainerMapper.constructor_arg('name')
    def name(self, builder, manager):
        return builder.name

    @NWBContainerMapper.object_attr("timestamps")
    def timestamps_attr(self, container, manager):
        ret = container.fields.get('timestamps')
        if isinstance(ret, TimeSeries):
            owner = ret
            curr = owner.fields.get('timestamps')
            while isinstance(curr, TimeSeries):
                owner = curr
                curr = parent.fields.get('timestamps')
            ts_builder = manager.build(owner)
            tstamps_builder = ts_builder['timestamps']
            ret = LinkBuilder(tstamps_builder, 'timestamps')
        return ret

    @NWBContainerMapper.constructor_arg("timestamps")
    def timestamps_attr(self, builder, manager):
        tstamps_builder = builder
        if isinstance(builder, LinkBuilder):
            target = builder.target
            return manager.construct(target.parent)
        else:
            return builder.data
