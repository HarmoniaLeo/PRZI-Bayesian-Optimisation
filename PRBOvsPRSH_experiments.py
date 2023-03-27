from utils import mutations,envs,PRSH_bayesian_paras,PRSH_paras
from BSE import market_session
import pandas as pd
from joblib import Parallel, delayed
import random

#envs = generate_environment(100)

repeats = 100
mutations = mutations
envs = envs

sup_ranges = [(100, 300, env) for env in envs]
dem_ranges = sup_ranges
spec = [('GVWY',20), ('ZIC',20), ('SHVR',20), ('SNPR',20), ('ZIP',20), ('PRSH',20),('PRBO',20)]
traders_spec = {'sellers':spec, 'buyers':spec}
start_time = 0
end_time = 1000
supply_schedules = [[{'from': start_time, 'to': end_time, 'ranges': [sup_range], 'stepmode': 'fixed'}] for sup_range in sup_ranges]
demand_schedules = [[{'from': start_time, 'to': end_time, 'ranges': [dem_range], 'stepmode': 'fixed'}] for dem_range in dem_ranges]
order_interval = 10
order_scheds = [{'sup': supply_schedule, 'dem': demand_schedule,'interval': order_interval, 'timemode': 'drip-poisson'} for supply_schedule,demand_schedule in zip(supply_schedules,demand_schedules)]

results = []

def an_env(env_id,exp):
    trialId = 'paired_' + str(env_id) + '_' + str(exp)
    buffer = 'results_buffer/' + trialId + '_avg_balance.csv'
    try:
        pd.read_csv(buffer,header=None)
    except Exception:
        tdump = open(buffer,'w')
        print("Start env{0}, exp{1}".format(env_id,exp))
        PRSH_bayesian_para = PRSH_bayesian_paras[env_id]  #K*Y(e),V*Y(e)
        PRSH_para = PRSH_paras[env_id]  #K*X(e),V*X(e),M*X(e)
        PRSH_bayesian_para = PRSH_bayesian_para[random.randint(0,len(PRSH_bayesian_para)-1)]    #random choosing parameter combination PRSH-Bayesian
        PRSH_para = PRSH_para[random.randint(0,len(PRSH_para)-1)]    #random choosing parameter combination for PRSH
        market_session(trialId, start_time, end_time, traders_spec, order_scheds[env_id], tdump, False, False,
        {"mutate_strat":mutations[PRSH_para[0]],"k":PRSH_para[1],"strat_eval_time":PRSH_para[2],"k_b":PRSH_bayesian_para[0],"strat_eval_time_b":PRSH_bayesian_para[1]})
        print("End env{0}, exp{1}".format(env_id,exp))
        tdump.close()

if __name__ == "__main__":

    Parallel(n_jobs=-1)(delayed(an_env)(env_id,exp) 
    for env_id in range(len(envs)) 
    for exp in range(repeats))

    # pbar = tqdm.tqdm(total = repeats * len(envs))
    for env_id in range(len(envs)): #each e
        for exp in range(repeats):  #each trial
            trialId = 'paired_' + str(env_id) + '_' + str(exp)
            buffer = 'results_buffer/' + trialId + '_avg_balance.csv'
            res = pd.read_csv(buffer,header=None)
            res = res.iloc[0]
            res = res.values.tolist()
            for j in range(len(res)):
                if res[j] == " PRSH":
                    res1 = res[j+3]
                if res[j] == " PRBO":
                    res2 = res[j+3]
            results.append([env_id,res1,res2])
                #os.remove(buffer)
                # pbar.update(1)

    # pbar.close()
    results = pd.DataFrame(results,columns=["env","profit1","profit2"])
    results.to_csv("results/PRBOvsPRSH_results.csv",index=None)