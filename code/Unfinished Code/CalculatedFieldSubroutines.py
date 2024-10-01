#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np

import pandas as pd


# In[1]:


def BinaryDrivingMode( chassis_df ):

    drive_mode_lst = chassis_df[ 'drivingMode' ].tolist()

    binary_drive_mode_lst = []
    
    for drive_mode in drive_mode_lst:

        if ( ( drive_mode == 'COMPLETE_MANUAL' ) or ( drive_mode == 'EMERGENCY_MODE' ) ):

            binary_drive_mode_lst.append( 0 )

        elif ( drive_mode == 'COMPLETE_AUTO_DRIVE' ):

            binary_drive_mode_lst.append( 1 )

        else:

            raise Exception( f'Unknown driving mode: { drive_mode }' )

    chassis_df[ 'BinaryDrivingMode' ] = binary_drive_mode_lst


# In[2]:


def TernaryDrivingModeTransition( time_sorted_chassis_df ):

    binary_drive_mode_lst = time_sorted_chassis_df[ 'BinaryDrivingMode' ].tolist()

    ternary_drive_mode_trans_lst = []
    
    for index in range( 1, len( binary_drive_mode_lst ) ):

        drive_mode_trans = binary_drive_mode_lst[ index ] - binary_drive_mode_lst[ index - 1 ]

        ternary_drive_mode_trans_lst.append( drive_mode_trans )

    ternary_drive_mode_trans_lst = [ 0 ] + ternary_drive_mode_trans_lst

    time_sorted_chassis_df[ 'TernaryDrivingModeTransition' ] = ternary_drive_mode_trans_lst


# In[3]:


def LatLonTotalStdDev( best_pose_df ):

    lat_stddev_lst = best_pose_df[ 'latitudeStdDev' ].tolist()

    lon_stddev_lst = best_pose_df[ 'longitudeStdDev' ].tolist()

    def planar_distance( x, y ): return ( x ** 2 + y ** 2 ) ** ( 1 / 2 )

    latlon_total_stddev_lst = []

    for lat_stddev, lon_stddev in zip( lat_stddev_lst, lon_stddev_lst ):

        latlon_total_stddev = planar_distance( lat_stddev, lon_stddev )

        latlon_total_stddev_lst.append( latlon_total_stddev )

    best_pose_df[ 'LatLonTotalStdDev' ] = latlon_total_stddev_lst


# In[14]:


def ChassisBestPoseMatchedTime( same_gmID_chassis_df, same_gmID_best_pose_df ):

    chassis_time_array = np.array( same_gmID_chassis_df[ 'time' ] )

    best_pose_time_array = np.array( same_gmID_best_pose_df[ 'time' ] )

    chassis_best_pose_matched_time_lst = []

    for chassis_time in chassis_time_array:

        time_diff_array = best_pose_time_array - chassis_time

        abs_time_diff_array = np.abs( time_diff_array )

        min_index = np.where( abs_time_diff_array == np.min( abs_time_diff_array ) )

        chassis_best_pose_matched_time = best_pose_time_array[ min_index ][ 0 ]

        chassis_best_pose_matched_time_lst.append( chassis_best_pose_matched_time )

    same_gmID_chassis_df[ 'ChassisBestPoseMatchedTime' ] = chassis_best_pose_matched_time_lst

    same_gmID_best_pose_df[ 'ChassisBestPoseMatchedTime' ] = same_gmID_best_pose_df[ 'time' ]


# In[1]:


def NormalizedTime( chassis_df ):

    chassis_time_array = np.array( chassis_df[ 'time' ] )

    normalized_chassis_time_array = chassis_time_array - np.min( chassis_time_array )

    chassis_df[ 'NormalizedTime' ] = list( normalized_chassis_time_array )


# In[4]:


def DeltaTime( time_sorted_chassis_df ):

    chassis_time_array = np.array( time_sorted_chassis_df[ 'time' ] )

    chassis_delta_time_array = np.diff( chassis_time_array )

    chassis_delta_time_list = list( chassis_delta_time_array )

    chassis_delta_time_list = [ chassis_delta_time_list[ 0 ] ] + chassis_delta_time_list

    time_sorted_chassis_df[ 'DeltaTime' ] = chassis_delta_time_list


# In[3]:


def Distance( time_sorted_chassis_df ):

    chassis_DeltaTime_array = np.array( time_sorted_chassis_df[ 'DeltaTime' ] ) * 1e-9 # seconds

    chassis_speedMps_array = np.array( time_sorted_chassis_df[ 'speedMps' ] ) # meters/second

    chassis_Distance_list = [] # meters

    for index in range( len( chassis_DeltaTime_array ) ):

        current_index_Distance = np.sum( chassis_DeltaTime_array[ : index ] * chassis_speedMps_array[ : index ] )

        chassis_Distance_list.append( current_index_Distance )

    time_sorted_chassis_df[ 'Distance' ] = chassis_Distance_list


# In[ ]:




