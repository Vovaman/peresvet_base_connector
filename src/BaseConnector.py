# base connector for Peresvet platform
# realizes common logic for all connectors
import json
from .consts import Errors, StrVals as sv

'''
Base assumptions for all connectors.
This code should work on python and micropython (for ESP32 and clones).
1) After instantiating connector has a tag list returned from platform
   as self.tags: array.
2) ...and all attributes of connector object from hierarchy in self.attrs: dict.
3) Each tag in list has attributes:
   prsSource - json contains info how to get tag data from source;
   prsValueTypeCode - code of tag data type:
        1 - int
        2 - float
        3 - строка
        4 - json
   prsValueScale - value from source is multiplied by this value;
   prsMaxDev - significiant deviation from the previous value; values are
        compared after multiplication to prsValueScale.
4) Base connector does not realize event-driven data read.
5) Connector's method `init` get path to config file saved in json-format.
   This file contains two keys:
   id - connector's id in hierarchy
   server - uri to platform, some like `ws://192.168.1.101:8002`
6) Due to specific controller realizations there is no `read_data` method
   in BaseController.
7) `_prepare_tags` method adds two keys to each tag in list:
   prev_value - tag's value that was previously sent to platform;
   cur_value - tag's value that was read on last read cycle;
   Each key is dict like:
   {
       "x": <int, timestamp in millisec>,
       "y": <Any: tag's value; type is according prsValueTypeCode and prsValueScale>
   }
8) There are no time functions due to specific hardware platforms.
'''
class BaseConnector:

    def __init__(self):
        '''
        Constructor can't be awaitable.
        Thus it is necessary to call `init` method after BaseConnector instantiating.
        '''
        self._connected = False
        self.tags = []
        self.attrs = {}
        self._ws = None

    async def init(self, config: str='config.json', ws=None) -> bool:
        '''
        This method is called after instantiating a variable as
        BaseConnector.
        '''
        if config is None:
            await self.send_error(Errors.CN_NO_CONFIG)
            return False

        try:
            f = open(config)
            self._conf = json.load(f)
        except:
            await self.send_error(Errors.CN_WRONG_CONFIG)

            return False
        f.close()

        self._ws = ws

        self._connected = await self._connect()
        #self._parse_config(config)

    async def _connect(self) -> bool:
        '''
        Method connects to platform using websocket.
        '''
        s = ""
        if self._conf[sv.server][-1] != "/":
            s = "/"
        if not await self._ws.handshake(
            f"{self._conf[sv.server]}{s}{self._conf[sv.id]}"):
            return False

        data = await self._ws.recv()
        try:
            data = json.loads(data)
        except:
            self.send_error(Errors.CN_WRONG_RESPONSE)
            return False

        self.attrs = await self._process_attrs(data[sv.attrs])
        self.tags = await self._process_tags(data[sv.tags])

    async def _process_attrs(self, attrs: dict) -> dict:
        '''
        Method processes connector's attributes, returned from platform
        '''
        return attrs

    async def _process_tags(self, tags):
        '''
        Method processes connector's tags returned from platform
        '''
        for tag in tags:
            tag[sv.prev_value] = {
                sv.x: None,
                sv.y: None
            }
            tag[sv.cur_value] = {
                sv.x: None,
                sv.y: None
            }

        return tags

    async def _send_error(self, error: dict):
        '''
        Method for error log.
        '''
        pass

    async def _write_tag_data(self, tags_block):
        '''
        Suppose tag data are sent to platform block by block.
        For instance, blocks may be devided by updateTime parameter.
        '''
        def set_val(val, tag):
            val[sv.y] = tag[sv.cur_value][sv.y]

            if tag[sv.cur_value][sv.x] is not None:
                val[sv.x] = tag[sv.cur_value][sv.x]

        data = {sv.data: []}
        for tag in tags_block:
            tag_data = {
                sv.tag_id: tag[sv.id],
                sv.data: []
            }

            val = {}
            if tag[sv.prev_value][sv.y] is None:
                if tag[sv.cur_value][sv.y] is None:
                    continue
                set_val(val, tag)

            else:
                if tag[sv.attrs][sv.prsValueTypeCode] in [1, 2]:
                    if abs(tag[sv.cur_value][sv.y] - tag[sv.prev_value][sv.y]) >= \
                        tag[sv.attrs][sv.prsMaxDev]:

                        set_val(val, tag)
                else:
                    if tag[sv.cur_value][sv.y] != tag[sv.prev_value][sv.y]:
                        set_val(val, tag)

            if val != {}:
                tag_data[sv.data].append(val)

                tag[sv.prev_value][sv.y] = tag[sv.cur_value][sv.y]
                tag[sv.prev_value][sv.x] = tag[sv.cur_value][sv.x]

                data[sv.data].append(tag_data)

        if self._ws.open():
            await self._ws.send(data)
        else:
            await self._connect()
