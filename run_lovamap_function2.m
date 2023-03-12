function [result] = run_lovamap_function2(full_file_path, folder_subtype, filename, output_path)

    % Input parameters
    voxel_size        = 2;
    voxel_range       = [1e7, 1e8]; % desired resolution
    crop_percent      = 1;          % percentage of the domain to analyze
    dip_percent       = 0.8;
    hall_cutoff       = 6;          % radius, in um
    shell_thickness   = 4;          % in um
    num_2D_slices     = 30;
    combine_edge_subs = true;       % set to false for real scaffolds

    % Run LOVAMAP
    [data, time_log] = LOVAMAP(full_file_path, voxel_size, voxel_range, crop_percent, dip_percent, ...
        hall_cutoff, shell_thickness, num_2D_slices, combine_edge_subs);

    result = struct();
    result.global = struct();
    result.nonsubs = struct();
    result.subs = struct();
    reuslt.isInteriorSub = true(data.Descriptors.Global.numSubs, 1);

    % 1. Reorganize global data
    global_fields = fieldnames(data.Descriptors.Global);
    num_global_desc = length(data.Descriptors.Global.names);
    result.global.names = struct();
    result.global.values = struct();

    for i = 1 : num_global_desc
        % First entry of `global_fields` contains the names of the descriptors
        result.global.names.(global_fields{i + 1}) = data.Descriptors.Global.names{i};
        result.global.values.(global_fields{i + 1}) = data.Descriptors.Global.(global_fields{i + 1});
    end

    % 2. Reorganize inter-subunit descriptor data
    nonsub_fields = fieldnames(data.Descriptors.NonSubs);
    num_nonsub_desc = length(data.Descriptors.NonSubs.names);
    result.nonsubs.names = struct();
    result.nonsubs.values = struct();

    for i = 1 : num_intersub_desc
        % First entry of `intersub_fields` contains the names of the descriptors
        result.nonsubs.names.(intersub_fields{i + 1}) = data.Descriptors.NonSubs.names{i};
        result.nonsubs.values.(intersub_fields{i + 1}) = data.Descriptors.NonSubs.(intersub_fields{i + 1});
    end

    % 3. Write out subunit descriptor data
    sub_fields = fieldnames(data.Descriptors.Subs);
    num_sub_desc = length(data.Descriptors.Subs.names);
    result.subs.names = struct();
    result.subs.values = struct();

    for i = 1 : num_sub_desc
        % First entry of `sub_fields` contains the names of the descriptors
        result.subs.names.(sub_fields{i + 1}) = data.Descriptors.Subs.names{i};
        result.subs.values.(sub_fields{i + 1}) = data.Descriptors.Subs.(sub_fields{i + 1});
    end

    % Extract information on which subunits are edge subunits
    for i = 1 : data.Descriptors.Global.numSubs
        result.isInteriorSub(i) = ~data.Subunits{i}.edge;
    end
end
