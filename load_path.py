import os

def load_path(pidx, eidx):
    expression_name = ['1_neutral', '2_smile', '3_mouth_stretch', '4_anger', '5_jaw_left', 
                    '6_jaw_right', '7_jaw_forward', '8_mouth_left', '9_mouth_right', 
                    '10_dimpler', '11_chin_raiser', '12_lip_puckerer', '13_lip_funneler', '14_sadness',
                    '15_lip_roll', '16_grin', '17_cheek_blowing', '18_eye_closed', '19_brow_raiser',
                    '20_brow_lower']

    root = '/Users/sjh/Desktop/1-150'

    model_name = '{0}/{1}_OK_OK'.format(root, pidx)+'/'+expression_name[eidx-1]+'.obj'

    model_save_name = '{0}/{1}_OK_OK'.format(root, pidx)+'/'+expression_name[eidx-1]+'_crop.obj'

    plyname = '{0}/{1}_OK_OK'.format(root, pidx)+'/'+expression_name[eidx-1]+'.ply'

    return model_name, model_save_name, plyname
    