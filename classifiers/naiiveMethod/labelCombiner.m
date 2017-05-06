%%%%%%%%%%%%%%%%%SECTION 1%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:size(features1,1)
    for j=1:size(features2,1)
        
        match = 1;
        for k=1:22
            if(features1(i,k) ~= features2(j,k))
                match = 0;
            end
        end
        
        if(match == 1)
            if(labels1(i,1) == 1 && labels2(j,1) ~= 1 )
                labels1(i,1) = labels2(j,1);
                labels2(j,1) = -1;
            else
                if(labels2(j,1) == 1 && labels1(i,1) ~= 1)
                    labels2(j,1) = labels1(i,1);
                    labels1(i,1) = -1;
                else
                    if(labels1(i,1) == 1 && labels2(j,1) == 1)
                        labels2(j,1) = -1;
                    end
                    if( (labels1(i,1) == 2 && labels2(j,1) == 3) || (labels1(i,1) == 3 && labels2(j,1) == 2) )
                        fprintf('hsEr: Features match but the labels dont match removed both items\n');
                        labels1(i,1) = -1;
                        abels2(j,1) = -1;
                    end
                        
                end
            end

        end
    
    end     
end


while(find(labels1 == -1))
    for i=1:size(labels1,1)
        if(labels1(i,1) == -1)
            features1(i,:) = [];
            labels1(i,:) = [];
            break
        end
    end
end


while(find(labels2 == -1))
    for i=1:size(labels2,1)
        if(labels2(i,1) == -1)
            features2(i,:) = [];
            labels2(i,:) = [];
            break
        end
    end
end







%%%%%%%%%%%%%%%%%SECTION 2%%%%%%%%%%%%%%%%%%%%%%%%%%

for i=1:size(features0,1)
    for j=1:size(features1,1)
        
        match = 1;
        for k=1:22
            if(features0(i,k) ~= features1(j,k))
                match = 0;
            end
        end
        
        if(match == 1)
            labels0(i,1) = labels1(j,1);
            labels1(j,1) = -1;
        end
    
    end     
end


for i=1:size(features0,1)
    for j=1:size(features2,1)
        
        match = 1;
        for k=1:22
            if(features0(i,k) ~= features2(j,k))
                match = 0;
            end
        end
        
        if(match == 1)
            labels0(i,1) = labels2(j,1);
            labels2(j,1) = -1;
        end
    
    end     
end


while(find(labels1 == -1))
    for i=1:size(labels1,1)
        if(labels1(i,1) == -1)
            features1(i,:) = [];
            labels1(i,:) = [];
            break
        end
    end
end


while(find(labels2 == -1))
    for i=1:size(labels2,1)
        if(labels2(i,1) == -1)
            features2(i,:) = [];
            labels2(i,:) = [];
            break
        end
    end
end


%%%%%%%%%%%%%%%%%SECTION 3 TESTING%%%%%%%%%%%%%%%%%%%%%%%%%%
for i=1:size(features0,1)
    for j=1:size(features1,1)
        
        match = 1;
        for k=1:22
            if(features0(i,k) ~= features1(j,k))
                match = 0;
            end
        end
        
        if(match == 1)
            fprintf('hsEr: there is a match btw featu0 and featu1\n');
            fprintf(i);
            fprintf(j);
        end
    
    end     
end

for i=1:size(features0,1)
    for j=1:size(features2,1)
        
        match = 1;
        for k=1:22
            if(features0(i,k) ~= features2(j,k))
                match = 0;
            end
        end
        
        if(match == 1)
            fprintf('hsEr: there is a match btw featu0 and featu2\n');
            fprintf(i);
            fprintf(j);
        end
    
    end     
end

for i=1:size(features1,1)
    for j=1:size(features2,1)
        
        match = 1;
        for k=1:22
            if(features1(i,k) ~= features2(j,k))
                match = 0;
            end
        end
        
        if(match == 1)
            fprintf('hsEr: there is a match btw featu1 and featu2\n');
            if(labels1(i,1) ~= labels2(j,1))
                fprintf('hsEr: and the labels dont match\n');
            end
            fprintf(i);
            fprintf(j);
        end
    
    end     
end



%%%%%%%%%%%%%%%%%SECTION 4 CombiningResults%%%%%%%%%%%%%%%%%%%%%%%%%
finalFeatures = vertcat(features0, features1);
finalFeatures = vertcat(finalFeatures, features2);

finalLabels = vertcat(labels0, labels1);
finalLabels = vertcat(finalLabels, labels2);

save('finalCombinedFeaturesAndLabels', 'finalFeatures', 'finalLabels');
