function nosetip = find_nosetip(node_xyz)
%*****************************************************************************80
%
%% find the nosetip with max Z.
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

if size(node_xyz, 1) == 3
    node_xyz = node_xyz';
end

[~, i] = max(node_xyz(:,3));

nosetip = node_xyz(i, :);

end