-- To change the query, scroll down to the `QUERY SECTION` and change
-- the parameters you're interested in.

-- BOILERPLATE, leave this alone!
SELECT distinct(obj_id), tag, field, camera_id, rplanet_mcmc, rplanet_mcmc_err, period
FROM hunterdet 
JOIN hunterdet_flags using(obj_id) 
JOIN nomad using(obj_id) 
WHERE peak_idx = 1

-- QUERY SECTION
AND hunterdet.tag LIKE '11OR_TAMTFA' 

-- standard cuts
AND sde != 0 
AND prob_rp < 0.1               -- inverted from normal
AND ntrans > 3
AND delta_chisq < -40
AND sn_red < -6
AND sn_ellipse < 6
AND npts_good > 1000
AND dilution_v between 0 and 25

-- select objects not already flagged as such
AND flag not in ('EB', 'EBLM', 'Blend', 'X')
AND followup_flag is null
--

order by sde desc
