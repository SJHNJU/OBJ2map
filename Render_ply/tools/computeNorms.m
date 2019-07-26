function [Nx, Ny, Nz] = computeNorms(im, scale)

tri = delaunay(im(:,1),im(:,2));
%-----------------------------------------


xmin = min(im(:,1));ymin = min(im(:,2));
xmax = max(im(:,1));ymax = max(im(:,2));

xscale = scale;yscale=scale;
[X1, Y1] = meshgrid(xmin:xscale:xmax,ymax:-yscale:ymin);%生成规则网格坐标X和Y,方向步长均取0.005

[Norm,~] = find_normals(im',tri'); Norm=Norm';

norm1=griddata(im(:,1),im(:,2),Norm(:,1),X1,Y1);
norm2=griddata(im(:,1),im(:,2),Norm(:,2),X1,Y1);
norm3=griddata(im(:,1),im(:,2),Norm(:,3),X1,Y1);
norm1=uint8(rescale(norm1,0,255));
norm2=uint8(rescale(norm2,0,255));
norm3=uint8(rescale(norm3,0,255));

[m, n] = size(norm1);
Nx = zeros(m, n, 3);Ny = zeros(m, n, 3);Nz = zeros(m, n, 3);
Nx(:,:,1) = norm1;Nx(:,:,2) = norm1;Nx(:,:,3) = norm1;
Ny(:,:,1) = norm2;Ny(:,:,2) = norm2;Ny(:,:,3) = norm2;
Nz(:,:,1) = norm3;Nz(:,:,2) = norm3;Nz(:,:,3) = norm3;

Nx = uint8(Nx);Ny = uint8(Ny);Nz = uint8(Nz);
end


function [normal,normalf] = find_normals(im,tri)

[im,tri] = check_face_vertex(im,tri);

nface = size(tri,2);
nvert = size(im,2);
normal = zeros(3, nvert);

% unit normals to the faces
normalf = crossproduct( im(:,tri(2,:))-im(:,tri(1,:)), ...
    im(:,tri(3,:))-im(:,tri(1,:)) );
d = sqrt( sum(normalf.^2,1) ); d(d<eps)=1;
normalf = normalf ./ repmat( d, 3,1 );

% unit normal to the vertex
normal = zeros(3,nvert);
for i=1:nface
    f = tri(:,i);
    for j=1:3
        normal(:,f(j)) = normal(:,f(j)) + normalf(:,i);
    end
end
% normalize
d = sqrt( sum(normal.^2,1) ); d(d<eps)=1;
normal = normal ./ repmat( d, 3,1 );

% enforce that the normal are outward
v = im - repmat(mean(im,1), 3,1);
s = sum( v.*normal, 2 );
if sum(s>0)<sum(s<0)
    % flip
    normal = -normal;
    normalf = -normalf;
end

end


function z = crossproduct(x,y)
% x and y are (m,3) dimensional
z = x;
z(1,:) = x(2,:).*y(3,:) - x(3,:).*y(2,:);
z(2,:) = x(3,:).*y(1,:) - x(1,:).*y(3,:);
z(3,:) = x(1,:).*y(2,:) - x(2,:).*y(1,:);
end


