function [model_name, model_save_dir, D_dir, Nx_dir, Ny_dir, Nz_dir, C_dir] = idx_to_path(pidx, eidx)

%*****************************************************************************80
%
%% Find model path according to the index of people and expression.
%
%  Licensing:
%
%    This code is distributed under the GNU LGPL license.
%
%  Modified:
%
%    10 Jane 2019
%
%  Author:
%
%    JiaHui She
%
root = '~/Desktop/1-150';
save_root = '~/Desktop/1-150ply';
D_map_save_root = '~/Desktop/1-150map/Depth_map';
Nx_map_save_root = '~/Desktop/1-150map/Nx_map';
Ny_map_save_root = '~/Desktop/1-150map/Ny_map';
Nz_map_save_root = '~/Desktop/1-150map/Nz_map';
C_map_save_root = '~/Desktop/1-150map/C_map';

expression{1}='neutral';expression{2}='smile';expression{3}='mouth_stretch';expression{4}='anger';expression{5}='jaw_left'; ...
expression{6}='jaw_right';expression{7}='jaw_forward';expression{8}='mouth_left';expression{9}='mouth_right';expression{10}='dimpler'; ...
expression{11}='chin_raiser';expression{12}='lip_puckerer';expression{13}='lip_funneler';expression{14}='sadness';expression{15}='lip_roll';...
expression{16}='grin';expression{17}='cheek_blowing';expression{18}='eye_closed';expression{19}='brow_raiser';expression{20}='brow_lower';



model_path = [root, '/', num2str(pidx), '_OK_OK/', num2str(eidx), '_', expression{eidx}, '.obj'];
model_name = [num2str(eidx), '_', expression{eidx}];
model_save_dir = [save_root, '/', num2str(pidx),  '_OK_OK/'];
D_dir = [D_map_save_root, '/', num2str(pidx), '_OK_OK/'];
Nx_dir = [Nx_map_save_root, '/', num2str(pidx), '_OK_OK/'];
Ny_dir = [Ny_map_save_root, '/', num2str(pidx), '_OK_OK/'];
Nz_dir = [Nz_map_save_root, '/', num2str(pidx), '_OK_OK/'];
C_dir = [C_map_save_root, '/', num2str(pidx), '_OK_OK/'];
end
