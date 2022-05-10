import os, pickle, torch, random
import yaml
import numpy as np 
import sys
path_here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(path_here)
sys.path.append('.')
from main.optimizer import BaseOptimizer
from chemutils import * 
from inference_utils import * 

class DSToptimizer(BaseOptimizer):

	def __init__(self, args=None):
		super().__init__(args)
		self.model_name = "dst"

	def _optimize(self, oracle, config):

		self.oracle.assign_evaluator(oracle)

		max_generations = config["max_generations"]
		population_size = config['population_size']
		lamb = config['lamb']
		topk = config['topk']
		epsilon = config['epsilon']

		start_smiles_lst = ['C1(N)=NC=CC=N1']
		model_ckpt = os.path.join(path_here, "pretrained_model/qed_epoch_4_iter_0_validloss_0.57661.ckpt")
		gnn = torch.load(model_ckpt)

		current_set = set(start_smiles_lst)
		while True:
			next_set = set() 
			for smiles in current_set:
				try:
					if substr_num(smiles) < 3: #### short smiles
						smiles_set = optimize_single_molecule_one_iterate(smiles, gnn)  ### optimize_single_molecule_one_iterate_v2
					else:
						smiles_set = optimize_single_molecule_one_iterate_v3(smiles, gnn, topk = topk, epsilon = epsilon)
					next_set = next_set.union(smiles_set)
				except:
					pass 
			smiles_lst = list(next_set)
			score_lst = self.oracle(smiles_lst)
			if self.finish:
				break
				
			smiles_score_lst = [(smiles, score) for smiles, score in zip(smiles_lst, score_lst)]
			smiles_score_lst.sort(key=lambda x:x[1], reverse=True)
			print(smiles_score_lst[:5], "Oracle num: ", len(self.oracle))

			# current_set = [i[0] for i in smiles_score_lst[:population_size]]  # Option I: top-k 
			current_set, _, _ = dpp(smiles_score_lst = smiles_score_lst, num_return = population_size, lamb = lamb) # Option II: DPP

			if self.finish:
				break