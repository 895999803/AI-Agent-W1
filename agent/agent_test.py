import agent_recommend as ac
import agent_reading as ar

if __name__ == '__main__':

    agent_recommend = ac.Agent_Recommend("machine learning")
    recommend = agent_recommend.run()
    agent_reading = ar.Agent_Reading(recommend[0]["url"])
    paper = agent_reading.run()
