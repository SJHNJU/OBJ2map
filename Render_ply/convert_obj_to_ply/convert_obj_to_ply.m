addpath('./OBJ_IO/');

for pidx = 1:75
    for eidx = 1:20
        [model_path, model_name, model_save_dir] = idx_to_path(pidx, eidx);
        
        if exist(model_path) == 0
            disp([model_path, ' does not exist']);
        else
            if exist(model_save_dir) == 0
                mkdir(model_save_dir);
            end

            disp(['Processing ', model_path, '...'])
            [ node_num, face_num, normal_num, order_max ] = obj_size(model_path);

            [ node_xyz, face_order, face_node, normal_vector, vertex_normal ] = ...
                obj_read ( model_path, node_num, face_num, normal_num, order_max );

            node_xyz = node_xyz';
            ptCloud = pointCloud(node_xyz);
            pcwrite(ptCloud,[model_save_dir, model_name, '.ply'],'Encoding','ascii');
            disp([model_save_dir, model_name, '.ply generated']);
        end
        
    end
end