
files = dir('*output*.csv');
nfiles = length(files);


filename = fullfile(files(1).name);
table = readtable(filename);

labels = table2array(table(:,1));

hints = table2array(table(:,3));


for i=2:(nfiles)
    
    filename = fullfile(files(i).name);
    table = readtable(filename);

    tempLabels = table2array(table(:,1));
    tempHints = table2array(table(:,3));
    
    
    labels = vertcat(labels, tempLabels);
    hints = vertcat(hints,tempHints);            
end

save('extractedHintsAndLabels', 'labels', 'hints');
        
        


        