from utils import envs
from BSE import market_session
import pandas as pd
from joblib import Parallel, delayed

#envs = generate_environment(100)
sup_ranges = [(100, 300, env) for env in envs]
dem_ranges = sup_ranges
spec = [('GVWY',20), ('ZIC',20), ('SHVR',20), ('SNPR',20), ('ZIP',20), ('PRBO',20)]
traders_spec = {'sellers':spec, 'buyers':spec}
start_time = 0
end_time = 1000
supply_schedules = [[{'from': start_time, 'to': end_time, 'ranges': [sup_range], 'stepmode': 'fixed'}] for sup_range in sup_ranges]
demand_schedules = [[{'from': start_time, 'to': end_time, 'ranges': [dem_range], 'stepmode': 'fixed'}] for dem_range in dem_ranges]
order_interval = 10
order_scheds = [{'sup': supply_schedule, 'dem': demand_schedule,'interval': order_interval, 'timemode': 'drip-poisson'} for supply_schedule,demand_schedule in zip(supply_schedules,demand_schedules)]
repeats = 100
ks = range(2,5)
elapses = range(5,9)
results = []

def an_env(env_id,k,elapse,exp):
    trialId = 'b_' + str(env_id)  + '_' + str(k) + '_'  + str(2**elapse) + '_' + str(exp)
    buffer = 'results_buffer/' + trialId + '_avg_balance.csv'
    try:
        pd.read_csv(buffer,header=None)
    except Exception:
        tdump = open(buffer,'w')
        print("Start env{0},  k{1}, elapse{2}, exp{3}".format(env_id,k,2**elapse,exp))
        market_session(trialId, start_time, end_time, traders_spec, order_scheds[env_id], tdump, False, False,{"k_b":k,"strat_eval_time_b":2**elapse})
        print("End env{0},  k{1}, elapse{2}, exp{3}".format(env_id,k,2**elapse,exp))
        tdump.close()

if __name__ == "__main__":

    Parallel(n_jobs=-1)(delayed(an_env)(env_id,k,elapse,exp) for env_id in range(len(envs)) for k in ks for elapse in elapses for exp in range(repeats))

    # pbar = tqdm.tqdm(total = repeats * len(envs) * len(ks) * len(elapses))
    for env_id in range(len(envs)): #each e
        for k in ks:    #each k
            for elapse in elapses:  #each v
                for exp in range(repeats):  #each trial
                    trialId = 'b_' + str(env_id)  + '_' + str(k) + '_'  + str(2**elapse) + '_' + str(exp)
                    buffer = 'results_buffer/' + trialId + '_avg_balance.csv'
                    res = pd.read_csv(buffer,header=None)
                    res = res.iloc[0]
                    res = res.values.tolist()
                    for j in range(len(res)):
                        if res[j] == " PRBO":
                            res = res[j+3]
                            break
                    results.append([env_id,k,2**elapse,res])
                    #os.remove(buffer)
                    # pbar.update(1)

    # pbar.close()
    results = pd.DataFrame(results,columns=["env","k","elapse","profit"])
    results.to_csv("results/PRBO_results.csv",index=None)