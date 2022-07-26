# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017-2018 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
Version of the AutonomousSequence.py example connecting to 10 Crazyflies.
The Crazyflies go straight up, hover a while and land but the code is fairly
generic and each Crazyflie has its own sequence of setpoints that it files
to.

The layout of the positions:
    x2      x1      x0

y3  10              4

            ^ Y
            |
y2  9       6       3
            |
            +------> X

y1  8       5       2



y0  7               1

"""
import time
import logging

import cflib.crtp
from cflib.crazyflie.swarm import CachedCfFactory
from cflib.crazyflie.swarm import Swarm
from cflib.crazyflie.swarm import LogConfig


from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.utils import uri_helper
from cflib.crazyflie.swarm import SyncCrazyflie
from cflib.crazyflie.swarm import SyncLogger

logging.basicConfig(filename="final_data.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)


# Change uris and sequences according to your setup
URI1 = 'radio://0/80/2M/E7E7E7E7E7'
URI2 = 'radio://0/100/2M/E7E7E7E7E7'
# URI3 = 'radio://0/70/2M/E7E7E7E703'
# URI4 = 'radio://0/70/2M/E7E7E7E704'
# URI5 = 'radio://0/70/2M/E7E7E7E705'
# URI6 = 'radio://0/70/2M/E7E7E7E706'
# URI7 = 'radio://0/70/2M/E7E7E7E707'
# URI8 = 'radio://0/70/2M/E7E7E7E708'
# URI9 = 'radio://0/70/2M/E7E7E7E709'
# URI10 = 'radio://0/70/2M/E7E7E7E70A'


z0 = 0.4
z = 0.8

x0 = 0
x1 = 0
x2 = -0.7

y0 = 0.6
y1 = -0.6
y2 = 0.4
y3 = 1.0

#    x   y   z  time
sequence1 = [
    (x0, y0, z0, 3.0),
    # (x0, y0, z, 30.0),
    # (x0, y0, z0, 3.0),
]

sequence2 = [
    (x0, y1, z0, 3.0),
    # (x0, y1, z, 30.0),
    # (x0, y1, z0, 3.0),
]

sequence3 = [
    (x0, y2, z0, 3.0),
    (x0, y2, z, 30.0),
    (x0, y2, z0, 3.0),
]

sequence4 = [
    (x0, y3, z0, 3.0),
    (x0, y3, z, 30.0),
    (x0, y3, z0, 3.0),
]

sequence5 = [
    (x1, y1, z0, 3.0),
    (x1, y1, z, 30.0),
    (x1, y1, z0, 3.0),
]

sequence6 = [
    (x1, y2, z0, 3.0),
    (x1, y2, z, 30.0),
    (x1, y2, z0, 3.0),
]

sequence7 = [
    (x2, y0, z0, 3.0),
    (x2, y0, z, 30.0),
    (x2, y0, z0, 3.0),
]

sequence8 = [
    (x2, y1, z0, 3.0),
    (x2, y1, z, 30.0),
    (x2, y1, z0, 3.0),
]

sequence9 = [
    (x2, y2, z0, 3.0),
    (x2, y2, z, 30.0),
    (x2, y2, z0, 3.0),
]

sequence10 = [
    (x2, y3, z0, 3.0),
    (x2, y3, z, 30.0),
    (x2, y3, z0, 3.0),
]

seq_args = {
    URI1: [sequence1],
    URI2: [sequence2],
    # URI3: [sequence3],
    # URI4: [sequence4],
    # URI5: [sequence5],
    # URI6: [sequence6],
    # URI7: [sequence7],
    # URI8: [sequence8],
    # URI9: [sequence9],
    # URI10: [sequence10],
}

# List of URIs, comment the one you do not want to fly
uris = {
    URI1,
    URI2,
    # URI3,
    # URI4,
    # URI5,
    # URI6,
    # URI7,
    # URI8,
    # URI9,
    # URI10
}

def log_stab_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    # logging.info(data)

def wait_for_param_download(scf):
    while not scf.cf.param.is_updated:
        time.sleep(1.0)
    print('Parameters downloaded for', scf.cf.link_uri)


def take_off(cf, position):
    take_off_time = 1.0
    sleep_time = 0.1
    steps = int(take_off_time / sleep_time)
    vz = position[2] / take_off_time

    print(vz)

    for i in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)


def land(cf, position):
    landing_time = 1.0
    sleep_time = 0.1
    steps = int(landing_time / sleep_time)
    vz = -position[2] / landing_time

    print(vz)

    for _ in range(steps):
        cf.commander.send_velocity_world_setpoint(0, 0, vz, 0)
        time.sleep(sleep_time)

    cf.commander.send_stop_setpoint()
    # Make sure that the last packet leaves before the link is closed
    # since the message queue is not flushed before closing
    time.sleep(0.1)


def run_sequence(scf, sequence):
    try:
        cf = scf.cf

        take_off(cf, sequence[0])
        for position in sequence:
            print('Setting position {}'.format(position))
            end_time = time.time() + position[3]
            while time.time() < end_time:
                cf.commander.send_position_setpoint(position[0],
                                                    position[1],
                                                    position[2], 0)
                time.sleep(1)
        land(cf, sequence[-1])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    cflib.crtp.init_drivers()

    logconf = LogConfig(name='gyro', period_in_ms=10)
    logconf.add_variable('ranging.distance0', 'float')
    # logconf.add_variable('ranging.distance2', 'float')
    # logconf.add_variable('ranging.distance3', 'float')
    # logconf.add_variable('ranging.distance5', 'float')
    # logconf.add_variable('gyro.x', 'FP16')
    # logconf.add_variable('gyro.y', 'FP16')
    # logconf.add_variable('gyro.z', 'FP16')

    factory = CachedCfFactory(rw_cache='./cache')
    with Swarm(uris, factory=factory) as swarm:
        # If the copters are started in their correct positions this is
        # probably not needed. The Kalman filter will have time to converge
        # any way since it takes a while to start them all up and connect. We
        # keep the code here to illustrate how to do it.
        # swarm.reset_estimators()

        # The current values of all parameters are downloaded as a part of the
        # connections sequence. Since we have 10 copters this is clogging up
        # communication and we have to wait for it to finish before we start
        # flying.
        print('Waiting for parameters to be downloaded...')
        swarm.parallel(wait_for_param_download)

        cf = swarm._cfs['radio://0/80/2M/E7E7E7E7E7']
        cf.log.add_config(logconf)
        logconf.data_received_cb.add_callback(log_stab_callback)
        logconf.start()
        swarm.parallel(run_sequence, args_dict=seq_args)

        logconf.stop()
