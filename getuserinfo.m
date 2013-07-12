archst  = computer('arch');

if strcmp(archst, 'maci64')
    name = getenv('USER');
    if strcmp(name, 'nick')
        directory = '/Users/nick/Dropbox/filesforNick/';
    elseif strcmp(name, 'Frank')
        directory = '/Users/Frank/Desktop/monkeylab/data/';
    elseif strcmp(name, 'zacharyabzug')
        directory = '/Users/zacharyabzug/Desktop/zackdata/';
    end
    slash = '/';
elseif strcmp(archst, 'win32') || strcmp(archst, 'win64')
    if strcmp(getenv('username'),'SommerVD') || ...
            strcmp(getenv('username'),'LabV') || ...
            strcmp(getenv('username'),'Purkinje') || ...
            strcmp(getenv('username'),'vp35')
        directory = 'C:\Data\Recordings\';
    elseif strcmp(getenv('username'),'DangerZone')
        directory = 'E:\data\Recordings\';
    elseif strcmp(getenv('username'),'Radu')
        directory = 'E:\Spike_Sorting\';
        githubdirectory = 'C:\Users\Radu\Documents\GitHub\';
    elseif strcmp(getenv('username'),'The Doctor')
        directory = 'C:\Users\The Doctor\Data\';
        githubdirectory = 'C:\Users\The Doctor\Documents\GitHub\';
    else
        directory = 'B:\data\Recordings\';
    end
    slash = '\';
end