from datetime import datetime, timedelta




class MatchCache():

    def __init__(self, loaded_once):
        self.loaded_once = loaded_once



class Agent():

    def __init__(self, agent):
        self.agent = agent
        self.c = {'Jett': 'Cloudburst', 'Reyna': 'Leer', 'Raze': 'Boom Bot', 'Yoru': 'Fakeout', 'Phoenix': 'Blaze', 'Neon': 'Fast Lane', 'Breach': 'Aftershock', 'Skye': 'Regrowth',
                  'Sova': 'Owl Drone', 'KAY/O': 'FRAG/MENT', 'Killjoy': 'Nanoswarm', 'Cypher': 'Trapwire', 'Sage': 'Barrier Orb', 'Chamber': 'Trademark', 'Omen': 'Shrouded Step',
                  'Brimstone': 'Stim Beacon', 'Astra': 'Gravity Well', 'Viper': 'Snake Bite', 'Fade': 'Prowler'}
        self.q = {'Jett': 'Updraft', 'Reyna': 'Devour', 'Raze': 'Blast Pack', 'Yoru': 'Blindside', 'Phoenix': 'Curveball', 'Neon': 'Relay Bolt', 'Breach': 'Flashpoint', 'Skye': 'Trailblazer',
                  'Sova': 'Shock Bolt', 'KAY/O': 'FLASH/DRIVE', 'Killjoy': 'Alarmbot', 'Cypher': 'Cyber Cage', 'Sage': 'Slow Orb', 'Chamber': 'Headhunter', 'Omen': 'Paranoia',
                  'Brimstone': 'Incendiary', 'Astra': 'Nova Pulse', 'Viper': 'Poison Cloud', 'Fade': 'Seize'}
        self.e = {'Jett': 'Tailwind', 'Reyna': 'Dismiss', 'Raze': 'Paint Shells', 'Yoru': 'Gatecrash', 'Phoenix': 'Hot Hands', 'Neon': 'High Gear', 'Breach': 'Fault Line', 'Skye': 'Guiding Light',
                  'Sova': 'Recon Bolt', 'KAY/O': 'ZERO/POINT', 'Killjoy': 'Turret', 'Cypher': 'Spycam', 'Sage': 'Healing Orb', 'Chamber': 'Rendezvous', 'Omen': 'Dark Cover',
                  'Brimstone': 'Sky Smoke', 'Astra': 'Nebula / Dissipate', 'Viper': 'Toxic Screen', 'Fade': 'Haunt'}
        self.x = {'Jett': 'Blade Storm', 'Reyna': 'Empress', 'Raze': 'Showstopper', 'Yoru': 'Dimensional Drift', 'Phoenix': 'Run It Back', 'Neon': 'Overdrive', 'Breach': 'Rolling Thunder',
                  'Skye': 'Seekers', 'Sova': "Hunter's Fury", 'KAY/O': 'NULL/CMD', 'Killjoy': 'Lockdown', 'Cypher': 'Neural Theft', 'Sage': 'Resurrection', 'Chamber': 'Tour De Force', 'Omen': 'From The Shadows',
                  'Brimstone': 'Orbital Strike', 'Astra': 'Astral Form / Cosmic Divide', 'Viper': "Viper's Pit", 'Fade': 'Nightfall'}

class Match():

    def __init__(self, input_json, index, name):
        """
        :param input_json: The data that is entered,
        :param index: The index of the match (0-4)
        :param name: The name of the main player requested.
        """

        self.data = input_json
        self.index = index
        self.data = self.data['data'][self.index]
        self.name = name
        # Player Data
        players = self.data['players']['all_players']
        for player in players:
            if player['name'] == name:
                self.puuid = player['puuid']
                self.team  = player['team']
                self.agent = player['character']
                self.level = player['level']
                self.rank = player['currenttier_patched']
                self.combat_score = player['stats']['score']
                self.kills = player['stats']['kills']
                self.deaths = player['stats']['deaths']
                self.assists = player['stats']['assists']
                self.headshots = player['stats']['headshots']
                self.bodyshots = player['stats']['bodyshots']
                self.legshots = player['stats']['legshots']
                ability_casts = player['ability_casts']
                self.times_ulted = ability_casts['x_cast']
                self.c_cast = ability_casts['c_cast']
                self.e_cast = ability_casts['e_cast']
                self.q_cast = ability_casts['q_cast']
                self.wide_card = player['assets']['card']['wide']
                self.agent_small_icon = player['assets']['agent']['small']
                break

        self.match_kills = []
        match_kills = self.data['kills']

        for kill in match_kills:
            if kill['victim_puuid'] == self.puuid:
                self.match_kills.append(kill)
            elif kill['killer_puuid'] == self.puuid:
                self.match_kills.append(kill)

        try:
            self.rounds_won = self.data['teams'][str(self.team).lower()]['rounds_won']
            self.rounds_lost = self.data['teams'][str(self.team).lower()]['rounds_lost']
            self.has_won_bool = self.data['teams'][str(self.team).lower()]['has_won']
        except KeyError:
            self.rounds_won = "X"
            self.rounds_lost = "X"
            self.has_won_bool = False

        try:
            if self.data['teams'][str(self.team).lower()]['has_won']:
                self.has_won = "won"
            else:
                self.has_won = "lost"
        except KeyError:
            self.has_won = "no teams"

        # Metadata
        self.map_name = self.data['metadata']['map']
        self.mode = self.data['metadata']['mode']
        self.game_start = datetime.fromtimestamp(self.data['metadata']['game_start'])
        self.game_end = self.game_start + timedelta(milliseconds=self.data['metadata']['game_length'])
        self.timestamp_start = self.data['metadata']['game_start']
        self.game_length_in_sec = self.data['metadata']['game_length'] / 1000
        self.server = self.data['metadata']['cluster']



    def __eq__(self, other):
        return self.__dict__ == other.__dict__






