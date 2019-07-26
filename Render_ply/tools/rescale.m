function y = rescale(x,a,b)
% rescale - rescale data in [a,b]
%
%   y = rescale(x,a,b);
%
%   Copyright (c) 2004 Gabriel Peyr¨¦

m = min(x(:));
M = max(x(:));

y = (b-a) * (x-m)/(M-m) + a;
end