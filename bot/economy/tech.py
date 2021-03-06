from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId


def can_research(bot, tech):
    if tech not in bot.state.upgrades and bot.can_afford(tech):
        if tech in [UpgradeId.ZERGGROUNDARMORSLEVEL2, UpgradeId.ZERGMISSILEWEAPONSLEVEL2, UpgradeId.ZERGFLYERWEAPONSLEVEL2, UpgradeId.ZERGFLYERARMORSLEVEL2]:
            if bot.units(UnitTypeId.LAIR).exists:
                return True
        elif tech in [UpgradeId.ZERGGROUNDARMORSLEVEL3, UpgradeId.ZERGMISSILEWEAPONSLEVEL3, UpgradeId.ZERGFLYERWEAPONSLEVEL3, UpgradeId.ZERGFLYERARMORSLEVEL3]:
            if bot.units(UnitTypeId.HIVE).exists:
                return True
        else:
            return True
    return False


def get_tech_to_research(bot, techs):
    for tech in techs:
        if can_research(bot, tech):
            return tech
    return None


def upgrade_tech(bot):
    if UpgradeId.GLIALRECONSTITUTION not in bot.state.upgrades and bot.can_afford(UpgradeId.GLIALRECONSTITUTION):
        if bot.units(UnitTypeId.ROACHWARREN).ready.exists and bot.units(UnitTypeId.LAIR).exists and bot.units(UnitTypeId.ROACHWARREN).ready.noqueue:
            bot.logger.debug("Researching Glial Reconstitution for roaches")
            return [bot.units(UnitTypeId.ROACHWARREN).ready.first.research(UpgradeId.GLIALRECONSTITUTION)]

    idle_chambers = bot.units(UnitTypeId.EVOLUTIONCHAMBER).ready.noqueue
    if idle_chambers:
        research_order = [
            UpgradeId.ZERGGROUNDARMORSLEVEL1,
            UpgradeId.ZERGGROUNDARMORSLEVEL2,
            UpgradeId.ZERGMISSILEWEAPONSLEVEL1,
            UpgradeId.ZERGMISSILEWEAPONSLEVEL2,
            UpgradeId.ZERGGROUNDARMORSLEVEL3,
            UpgradeId.ZERGMISSILEWEAPONSLEVEL3
        ]
        tech = get_tech_to_research(bot, research_order)
        if tech:
            bot.logger.debug(f"Researching {tech}")
            return [idle_chambers.first.research(tech)]

    idle_spire = bot.units(UnitTypeId.SPIRE).ready.noqueue
    if idle_spire:
        research_order = [
            UpgradeId.ZERGFLYERWEAPONSLEVEL1,
            UpgradeId.ZERGFLYERWEAPONSLEVEL2,
            UpgradeId.ZERGFLYERARMORSLEVEL1,
            UpgradeId.ZERGFLYERARMORSLEVEL2,
            UpgradeId.ZERGFLYERWEAPONSLEVEL3,
            UpgradeId.ZERGFLYERARMORSLEVEL3
        ]
        tech = get_tech_to_research(bot, research_order)
        if tech:
            bot.logger.debug(f"Researching {tech}")
            return [idle_spire.first.research(tech)]

    return []
