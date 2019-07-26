clear all; clc; close all
addpath('tools')

bad_image_people_index = [];

pidx = 11;
eidx = 13;
    if isempty(find(bad_image_people_index == pidx, 1))
        [model_name, model_dir, D_dir, Nx_dir, Ny_dir, Nz_dir, C_dir] = idx_to_path(pidx, eidx);
        model_path = [model_dir, model_name, '.ply'];

        if exist(model_path) == 0
            disp([model_path, ' does not exist']);
        else
            disp(['Rendering ', model_path, '...']);
            
            ptCloud = pcread(model_path);
            Location = ptCloud.Location;
            node_xyz = Location;
            
            y_ = -100;
            new_node_xyz = node_xyz(node_xyz(:, 2) > y_, :);
            new_node_xyz = new_node_xyz(new_node_xyz(:, 1) < 95, :);
            new_node_xyz = new_node_xyz(new_node_xyz(:, 2) < 150, :);
            
            pcshow(new_node_xyz),xlabel('x'),ylabel('y'),zlabel('z');

            nosetip = find_nosetip(new_node_xyz);
%             nosetip = [2.6, -9, 66.36];
            radius = 90;    % 80/70/100
            [indices,~] = findNeighborsInRadius(ptCloud, nosetip, radius);
            ptCloud = select(ptCloud,indices);
            
            pcshow(ptCloud);    
% % % %             
%             im = ptCloud.Location;
%             D = computeDepth(im, 0.3);
%             [Nx, Ny, Nz] = computeNorms(im, 0.3);
%             C = computeCurvature(im, 0.3);
%             
%             if exist(D_dir) == 0
%                 mkdir(D_dir)
%             end
%             if exist(Nx_dir) == 0
%                 mkdir(Nx_dir)
%             end
%             if exist(Ny_dir) == 0
%                 mkdir(Ny_dir)
%             end
%             if exist(Nz_dir) == 0
%                 mkdir(Nz_dir)
%             end
%             if exist(C_dir) == 0
%                 mkdir(C_dir)
%             end
%             
%             imwrite(D, [D_dir, '/', model_name, '.png']);
%             imwrite(Nx, [Nx_dir, '/', model_name, '.png']);
%             imwrite(Ny, [Ny_dir, '/', model_name, '.png']);
%             imwrite(Nz, [Nz_dir, '/', model_name, '.png']);
%             imwrite(C, [C_dir, '/', model_name, '.png']);
%             
%             disp([model_path, ' is rendered'])

        end
    else
        disp(['Number ', num2str(pidx), ' is bad image'])

    end
  