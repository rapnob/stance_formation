LOGLEVEL = WARNING

init:
	mkdir -p data/cs/{raw,interim/result} data/common

data/cs/config.json:
	jo bugfix10d@F > $@

data/%/raw:
	mkdir -p data/$*/raw/ data/$*/interim/ data/$*/result/

data/cs/raw/cs.pickle: data/cs/raw
	cp /home/cs/covid/ASONAM2022_journal/data/alldf.pickle $@

data/%/interim/time_series_counter.pickle: data/%/raw/input.pickle
	python src/datatest.py $< data/$*/interim/unique_users.pickle $@ data/$*/interim/time_series_counter_old.pickle  data/$*/interim/time_series_counter_old2.pickle

data/%/interim/time_series_counter_old.pickle: data/%/interim/time_series_counter.pickle

data/%/interim/time_series_counter_old2.pickle: data/%/interim/time_series_counter.pickle

data/%/interim/unique_users.pickle: data/%/interim/time_series_counter.pickle

data/%/interim/selected_users.pickle: data/%/config.json data/%/interim/unique_users.pickle data/%/interim/time_series_counter.pickle
	python src/selected_users.py --config $^ $@

data/%/interim/edges.csv: data/%/interim/selected_users.pickle
	python src/make_edges.py $< $@ --log=${LOGLEVEL}

data/%/interim/edges_allobjtype.csv: data/%/interim/selected_users.pickle
	python src/make_edges_allobjtype.py $< $@ --log=${LOGLEVEL}

data/%/interim/A2B.pickle: data/%/interim/selected_users.pickle
	python src/toposneg.py $< $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_A2B_before_overtime.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_A2B_overtime.py $^ $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_A2B_before.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_A2B.py $^ $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_n2p_before.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_before.py $^  0  1 $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_n2a_before.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_before.py $^  0 -1 $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_p2n_before.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_before.py $^  1  0 $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_p2a_before.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_before.py $^  1 -1 $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_a2n_before.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_before.py $^ -1  0 $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_a2p_before.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_before.py $^ -1  1 $@ --log=${LOGLEVEL}

data/%/interim/cp_targets_n2n_before.pickle: data/%/interim/edges.csv data/%/interim/A2B.pickle
	python src/cp_target_before.py $^  0  0 $@ --log=${LOGLEVEL}

data/%/interim/cp_urls_n2p_before.pickle: data/%/raw/input.pickle data/%/interim/A2B.pickle
	python src/cp_url_before.py $^  0  1 $@

data/%/interim/cp_urls_n2a_before.pickle: data/%/raw/input.pickle data/%/interim/A2B.pickle
	python src/cp_url_before.py $^  0 -1 $@

data/%/interim/cp_urls_p2n_before.pickle: data/%/raw/input.pickle data/%/interim/A2B.pickle
	python src/cp_url_before.py $^  1  0 $@

data/%/interim/cp_urls_p2a_before.pickle: data/%/raw/input.pickle data/%/interim/A2B.pickle
	python src/cp_url_before.py $^  1 -1 $@

data/%/interim/cp_urls_a2p_before.pickle: data/%/raw/input.pickle data/%/interim/A2B.pickle
	python src/cp_url_before.py $^ -1  1 $@

data/%/interim/cp_urls_a2n_before.pickle: data/%/raw/input.pickle data/%/interim/A2B.pickle
	python src/cp_url_before.py $^ -1  0 $@

data/%/result/overmonths_n2p.pickle: data/%/interim/cp_urls_n2p_before.pickle
	python src/overmonths.py $< $@

data/%/result/overmonths_n2a.pickle: data/%/interim/cp_urls_n2a_before.pickle
	python src/overmonths.py $< $@

data/%/result/overmonths_p2n.pickle: data/%/interim/cp_urls_p2n_before.pickle
	python src/overmonths.py $< $@

data/%/result/overmonths_p2a.pickle: data/%/interim/cp_urls_p2a_before.pickle
	python src/overmonths.py $< $@

data/%/result/overmonths_a2p.pickle: data/%/interim/cp_urls_a2p_before.pickle
	python src/overmonths.py $< $@

data/%/result/overmonths_a2n.pickle: data/%/interim/cp_urls_a2n_before.pickle
	python src/overmonths.py $< $@

data/%/result/attribute_n2p.n2p_vs_n2a.pickle: data/%/interim/cp_targets_n2p_before.pickle data/%/interim/cp_targets_n2a_before.pickle
	python src/chi_user.py $^ $@.tmp --log=${LOGLEVEL}
	mv $@.tmp $@

data/%/result/attribute_n2a.n2p_vs_n2a.pickle: data/%/interim/cp_targets_n2a_before.pickle data/%/interim/cp_targets_n2p_before.pickle
	python src/chi_user.py $^ $@.tmp --log=${LOGLEVEL}
	mv $@.tmp $@


data/%/interim/chi_results_df.pickle: data/%/interim/cp_targets_n2p_before.pickle data/%/interim/cp_targets_n2a_before.pickle data/%/interim/cp_targets_n2n_before.pickle
	python src/chitest_shared_user.py $^ $@

data/%/result/attributes_df.pickle: data/%/interim/chi_results_df.pickle data/common/uid2desc_fromT.pickle data/common/uid2desc_fromRMQ_06to08.pickle data/common/uid2desc_fromRMQ_09to10.pickle
	python src/shared_user_attributes.py $< $@

data/%/interim/chi_results_overtime_df.pickle: data/%/interim/cp_targets_A2B_before_overtime.pickle
	python src/chitest_shared_user_overtime.py $< $@ --log=${LOGLEVEL}

data/%/result/attributes_overtime_df.pickle: data/%/interim/chi_results_overtime_df.pickle 
	python src/shared_user_attributes_overtime.py $< $@

data/%/graph/nodes:
	mkdir -p $@

SPAN=06-1-10
data/%/graph/nodes/${SPAN}_nodes_new.csv: data/%/interim/time_series_counter.pickle data/%/graph/nodes
	python src/graph/make_nodedata.py $< ${SPAN} $@.tmp --log ${LOGLEVEL}
	mv $@.tmp $@

data/%/graph/graphml/${SPAN}_30.graphml: data/%/graph/nodes/${SPAN}_nodes_new.csv
	python src/graph/make_graphml.py $< ${SPAN} $@

all:
	make data/cs/result/{overmonths_{n2p,n2a,a2p,a2n,p2a,p2n},attributes_df}.pickle 

.SECONDARY:
