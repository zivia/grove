import constraint
import lookup
import entity as e

from utils import rand


class Simulation:

    """
    A simple simulator designed to be used with GESwarm (Grammatical Evolution Swarm). Parse trees containing a set of
    rules dictate the control flow of the simulation. Rules contain a list of preconditions, behaviors, and actions.
    Together these rules may lead to interesting behaviors.

    For more information about GESwarm, see the article (http://dl.acm.org/citation.cfm?id=2463385).
    """

    def __init__(self, duration=1000, environment=None, entities=None, parse_tree=None, produce_output=True):

        self.duration = duration
        self.environment = environment
        self.entities = entities
        self.parse_tree = parse_tree
        self.produce_output = produce_output
        self.state_archive = []

        self.agents = filter(lambda x: isinstance(x, e.SimAgent), self.entities)

        # Initial behavioral state for each entity.
        for agent in self.agents:

            agent.behavior = lookup.b[self.parse_tree.default_behavior.id_behavior]

    def save_state(self, entity=None):

        """
        Saves the current state of all entities to the state archive.
        :param entity: The entity to add to the state archive
        """

        self.state_archive.append(entity.to_csv())

    def execute_step(self):

        """
        Executes a single step of the simulation.
        """

        if all([agent.time < self.duration for agent in self.agents]):

            for agent in self.agents:

                if agent.time >= self.duration:

                    agent.done = True
                    continue

                agent = self.process_rules(agent)

            return True

        else:

            return False

    def execute_all(self):

        """
        Executes the simulation.
        """

        while all([agent.time < self.duration for agent in self.agents]):

            for agent in self.agents:

                if agent.time >= self.duration:

                    agent.done = True
                    continue

                agent = self.process_rules(agent)

    def process_rules(self, agent):

        """
        Processes the rule set on a given entity.
        :param agent: The agent to evaluate with the rule set.
        :return: The entity, with possible updates.
        """

        hit = False

        for rule in self.parse_tree.rules:

            # Gather all precondition functions contained in the current rule.
            preconditions = [lookup.pc[pc.id_precondition] for pc in rule.preconditions if pc]
            behaviors = [lookup.b[b.id_behavior] for b in rule.behaviors if b]

            # Evaluate the current entity.
            pc_check = all([precondition(agent, self.entities, self.environment) for precondition in preconditions])
            b_check = any([agent.behavior is behavior for behavior in behaviors])

            if pc_check and b_check:

                for action in rule.actions:

                    if action.id_action in lookup.b:

                        action_b = lookup.b[action.id_action]

                        if rand.uniform(0.0, 1.0) <= action.prob:

                            if (agent.behavior in constraint.blacklist and action_b not in constraint.blacklist[agent.behavior]) or agent.behavior not in constraint.blacklist:

                                hit = True

                                agent = lookup.b[action.id_action](agent, self.entities, self.environment)
                                agent.behavior = lookup.b[action.id_action]

                                if self.produce_output:

                                    self.save_state(agent)

                    else:

                        print self.parse_tree

        if not hit:

            agent = agent.behavior(agent, self.entities, self.environment)
            agent.time += 1

            if self.produce_output:

                self.save_state(agent)

        return agent
