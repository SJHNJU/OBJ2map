function Texturemap = computeTextrue(ptCloud, scale)

vertex = ptCloud.Location;
im = vertex;

xmin = min(im(:,1));ymin = min(im(:,2));
xmax = max(im(:,1));ymax = max(im(:,2));
xscale = scale;yscale=scale;

X1 = xmin:xscale:xmax;rows = length(X1);X1(rows+1) = xmax;
Y1 = ymin:yscale:ymax;cols = length(Y1);Y1(cols+1) = ymax;

Tmap = zeros(rows, cols);
for i = 1:rows
    for j = 1:cols
            centerPoint = [(X1(i)+X1(i+1))/2, (Y1(j)+Y1(j+1))/2];
            idx = intersect(find(vertex(:,1) > centerPoint(1)-1.8*scale), find(vertex(:,1) < centerPoint(1)+1.8*scale));
            idy = intersect(find(vertex(:,2) > centerPoint(2)-1.8*scale), find(vertex(:,2) < centerPoint(2)+1.8*scale));
            id = intersect(idx, idy);
            if isempty(id)
                Tmap(i,j) = -1;
            elseif length(id) == 1
                Tmap(i,j) = id(1);
            else
                vertex1 = vertex(id, 1:2);
                c = repmat(centerPoint, length(id), 1);
                dis = sum((vertex1 - c).^2, 2);
                [~, k] = min(dis);
                Tmap(i,j) = id(k);
            end
    end
end


Texturemap = zeros(rows, cols, 3);
for i =1:rows
    for j =1:cols
        if Tmap(i,j) ~= -1
            Texturemap(i, j, :) = ptCloud.Color(Tmap(i,j), :);
        end
    end
end
Texturemap = uint8(Texturemap);
hold on 

end


