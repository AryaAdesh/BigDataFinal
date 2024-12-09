import google.generativeai as genai

# Configure the API
GOOGLE_API_KEY = 'AIzaSyDShtModtneL_-c-UxGECg6e0DYs3Xpen8'
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def summarize_and_generate_key_phrases(texts):
    results = []
    # Generate summary
    combined_text = "\n".join(texts)
    summary_prompt = f"""
            You are an AI machine working for Twitter. You are given the following Twitter threads.
            Now your job is read all the twitter threads and summarize the thread for a layman user Please make the summary in 3-4 sentences..: 
            
            
            {combined_text}
            """
    summary_response = model.generate_content(summary_prompt)
    summary = summary_response.text

    # Generate key phrases
    phrases_prompt = f"""
    You are an analyst preparing the key trends. Analyse the following the texts and summarize the into a theme of 2-3 words: 
    
    
    {combined_text}
    """
    phrases_response = model.generate_content(phrases_prompt)
    key_phrases = phrases_response.text

    results.append({
        'summary': summary,
        'key_phrases': key_phrases
    })
    return results


# Example usage
# c1 = ["Virginia's 2025 election is incredibly important, and I'm worried that most people won't even realize that an off off election year (not even the midterm elections year, but an odd number year) is so very important. The governor's race is competitive and there is no incumbent, lots of work to do.", 'Trump likes Al Qaida .   They endorsed him last elections!!', 'This is what Putin gets for messing with Countries elections.', 'Goddam I always forget the hashtags!!!\n\n#electionhacking\n#election\n#democracy\n#elections', "Truth! Also I see everyone saying 'how dems went wrong' & messaging & no one discussing how gutting the VRA & taking jim crow era voting suppression national affected the last 3 elections, plus bomb threats! It's crazy to me that no one is talking about that", 'Dems lost the least of any incumbent party globally.\n\nEvery single incumbent party *across the globe* did terribly in elections.\n\nHow are folks turning this into "Dems historically failed"?\n\nYou want accountability? Run for office.\n\nOr convince your fellow voter not to vote for fascism.', 'They still haven’t figured out that THEY are the swamp he wants to drain. He will set them up to be screwed in their next elections and then take the credit for doing what he said he’d do.', "Mostly agree. Gotta get get big money out of elections and out of politics first.  That's a large hill to climb.  And it shouldn't be.", 'Sunday Power Play:\n1. Dept of Elections verified the initial signatures of \n@joelengardio.bsky.social recall, opening the door to an ugly political fight\n2. @sfzoo.bsky.social leadership uses pandas to "threaten" supervisors, prompting Melgar, Chan to fight back\n\nlink.sfstandard.com/view/6436ea0...', 'Instead of buying elections why couldn’t billionaires fund a second season of Scavengers Reign? 😭', 'It’s part of Project2025, end all elections! Citizens aren’t smart enough to vote, billionaires will decide & choose who rules America!', 'I understand the cynicism, but from what I’ve seen none of the major rebel factions are pushing for sectarian conflict. There’s good reason to hope that Syria’s future path is a spectrum from Iraq-style dysfunction to Ireland-style “civil war politics” shaping regular elections.', 'Term limits go directly against democracy by voiding the voting right of we the people to select our representatives.  What is needed is the overturn of the "Citizens United" court ruling to remove money from politics and make elections fair!', 'All precedents have been rendered meaningless by Donald coming back into power. There is nothing holding him accountable for anything he chooses to do. I’ll be relieved if we have elections again ever.', 'fun fact: reagan was elected just 3 years after the last time a guillotine was used', "The post office tests mail delivery by occasionally sending through brought orange plastic cards. If they don't go through, somebody gets fired. We should do that with elections too. Some of the ballots should be safeguard ballots and if they don't show up where they belong, it highlights a problem.", 'It is\nVote in state and local elections as well as the big ones', 'Oh that’s cute.You really think there’s going to be more elections?You really think heritage foundation,southern baptists,evangelicals,catholics,billionaires and maga gop didn’t sell us to Russia?cabinet nominees are mandated to destroy our institutions,chaos is coming-guns will be traded for food.', "He has commented several times that he has no intention of ever leaving office or holding presidential elections again. People who say he was 'just joking' are delusional.", "Our constitution and government honor elections and peaceful transfer of power.\nWe are not at liberty to prevent Trump from assuming office because we can't stand him. Any more than they were at liberty to prevent Biden from doing so. \nThat was my point.", 'We don’t need to trim social programs for low income people, disabled, elderly, or veterans.\nWe need to make the non-tax paying motherfuckers #PayTheirFairShare.\nAnd stop buying Supreme Court justice seats and presidential elections‼️', 'Can Palestinians in the West Bank vote in Israeli elections?', 'We don’t need to trim social programs for low income people, disabled, elderly, or veterans.\nWe need to make the non-tax paying motherfuckers #PayTheirFairShare.\nAnd stop buying Supreme Court justice seats and presidential elections‼️', 'Russia has definitely been proven to have had a hand in many of them. They interfered in the Georgian, Romanian, and Moldovan elections. They definitely are backing Hungary and Belorus.', 'I believe there are 3 House elections coming up that will desperately need Democrats to come out for in full force. Every seat that we deny the GOP makes we the people that much stronger. So get out and vote. Take your neighbors to the polls with you. Vote Blue.', 'Élections provinciales en 2026 | Le ministre de la Santé, Christian Dubé, n’a pas l’intention de se représenter\n\n#lapresse #manchettes ', " Elon is not only a visionary, he can plan the future. He seems to have bought Twitter only to help Trump so that he can take full advantage of his Presidency. India's Modi and ruling party similarly planted  fundamentalists in media, courts, audit institutions of India and won elections post 2014.", 'I support Democrats in national elections because I’m a team player and I know how math works, but to say the 2024 election hasn’t severely eroded whatever faith I still had in our institutions and the party establishment would be a massive understatement.', "14.\nNo money in politics so all can become a politician & the PM after a while in politics. Elections,both local & federal are payed by our govt. That way officials dont get the I have to do this to pay back my donors instead of make proper bills into laws ppl need & like,tho it's high taxes here..", 'Totally, however the corporate stain in the party is what lost them two elections in the past 10 years. If there’s any time the Democratic Party were to change course it would be now. Especially if more Democratic aligned politicians run as independent over Democrats. (Which I still have doubts.)', 'I missed this in September. \nBiden signed Executive Order 13848 on Sept 9, 2024 for it\'s continuation.\n\n"Notice on the Continuation of the National Emergency With Respect to Foreign Interference in or Undermining Public Confidence in United States Elections"', 'There will be no free fair elections in 2028, are you daft?', 'I AGREE WITH YOU. AND THEY WILL KEEP LOOSING ELECTIONS.', 'I found this map in a USA Today article and thought it was interesting. Turnout was still higher than most elections in recent years, but dropped off in most areas compared to 2020. \nSource: www.usatoday.com/story/graphi...', "www.newsobserver.com/opinion/arti...\nThis op ed by Bob Hall, long time director of Democracy North Carolina is enlightening.  He interviewed a dozen voters on Griffin's challenge list.  The NC Board of Elections meets at 12:30 PM Wednesday to consider Griffin's 60,000 challenges and protests", 'It’s playing out now… \n\nWhat happened yesterday in Syria 🇸🇾 is the plan, when Biden stepped down, Trump said he doesn’t need votes.. Elon programmed all voting machines all over the world using 4.9666% win for the all the elections. Romania 🇷🇴 \nSouth Korea.', "New elections that are free & fair don't take place under oppressive dictatorial rule. The sun shines after the storm...not during it", "Before you vote in any other elections, if we have any other elections, please educate yourself. Or just don't vote if you can't be bothered to educate yourself.", 'Honestly it’s better than buying elections. Though they should throw some money towards the arts too', "It took 24 years after being elected to achieve that, and it took 10 or so years for enough of the population to believe they need to oust Assad. This after he was widely 'confirmed' in an uncontested 'election'. Let's see if we suddenly lose valid elections in 2-4 years, for a start.", 'No, it’s the party line!\nHowever independents & green candidates have inroads in the recent federal elections, the right wing of Australian politics is considered a joke at this time, as one politician said ‘A drovers dog could win the next election’', "If more Democrats turned out and they won elections, the SCOTUS wouldn't be where it is.", "(3) Elections can't be held at the drop of a hat anywhere (18 months is not very much time), much less a country whose gov't has spent a decade systematically destroying records. Until the new constitution is drafted, it won't even be clear who runs elections or what the parameters are. (4/n)", 'You are humping for murdering the vulnerable.  That is what "not winning elections" means, you entitled bint.\nThat is a you thing. \nYou are humping for communism and have never heard of Ernst Thälmann nor the Molotov-Ribbentrop Pact nor the gulags.\nRead an actual history book.', "Wow, that's a big move! 🇺🇸 Ensuring fair elections is crucial.", "i told y'all we weren't gonna have any more elections after this one. Good job, America.", 'The evidence is sitting in the fukton county elections office.', "No it doesn't it just needs the Supreme Court to decide if its really constitutional. The supreme court could decide the 14th amendment wasn't properly ratified. Along with the 22nd Amendment. Along with elections.", 'Where is THE RESISTANCE? We used to be a beacon for democracy, ready to fight any foe threatening our freedoms. Instead we allowed rich oligarchs, some foreign, to literally buy our election and install a fascist convicted felon as president. If we don’t fight to win upcoming elections, we’re dead.', 'This is not enough time for a transition period that includes drafting a new constitution and holding elections given what Syrians have endured. There are so many other efforts that must happen alongside drafting and elections if those acts are to have any lasting effect: (1/n)', 'Love you, but the republican party has been stacking local elections, school boards, and judges for decades. Hipocracy is their normal.', '🗳️ Day 18 of #30DaysOfFLCode: Deleting an election in the Voting App is now easier than ever!\n\n✨ How? Just delete the election’s JSON file from the elections folder, and the app automatically removes it from everywhere.\n\nlucaslopes.me/voting\n\n#SyftBox #OpenMined #EVoting #PrivacyTech #Collaboration', 'He can buy three elections with that money 😳', ' volunteer for runoff and special elections across the country. Find opportunities to volunteer here: docs.google.com/spreadsheets...', 'Nations held their breath during our last elections to see if his 1st presidency was a fluke. We failed by reelecting him. Countries are moving on. USA is no longer reliable as an ally. New alliances are being forged. NATO is being overhauled without USA as a ruling/guiding body. que sera sera', 'I\'ll loathe trump BECAUSE we\'re saddled with it again, BECAUSE folks like you label things "too progressive" and the Democrats then parade around with Liz Cheney, and brag about the enforcement from her WAR CRIMINAL FATHER.\n\nFFS.\n\nYour "snark" is costing The People elections.', "Absolutely NOT. Everyone hates the second place person. Never works well most elections. Stop trying to propose new structures when we don't even know what happened yet.", 'During the campaign the slit above it\'s chin: "Didn\'t need any more votes."\nMusky took care of that.\n\nNo more elections - some didn\'t understand or care. \nWhy many of "US" got out and \n🗳 \'ed 💙 for "WE" knew it may \nbe our last time!\n#IAMTHE92PERCENT', "I think we need to have a serious discussion about whether the Lone Star resurgence is because of the party itself or just Beto, because the party consistently does way worse whenever he's not on the ballot.", 'Labour Party Inaugurates Katsina Committee to Strengthen Unity, Strategy for\xa02027\n\nThe Katsina State Chapter of the Labour Party has inaugurated a 12-member committee to address communication gaps between the party’s executive council and its members following the 2023 general elections. Leadership…', 'How many elections do we have to lose to realize Democrats messaging needs a gigantic overhaul? We have been polite, acquiescing and suckers thinking R’s will behave the same way. They haven’t and we are sucking hind tit', '"As Republicans, if you think you are going to change very substantially for the worse Medicare, Medicaid, and Social Security in any substantial way, and at the same time you think you are going to win elections, it just really is not going to happen... .', '🌟 Day 17 of #30DaysOfFLCode: Solved a tricky Vue.js reactivity issue to show live election & vote counts in the app! Results So Far:\n- Total Elections: 7\n- Total Votes: 21\n\nGrateful to the OpenMined Show & Tell for the traction! This is just the start\n\nlucaslopes.me/voting\n\n#SyftBox #EVoting #VueJS', 'OMG: Trump plan to ELIMINATE future elections is exposed\nDemocracy Watch with Brian Tyler Cohen Episode 154: \n\nSuccessful elections protection attorney Marc Elias discusses a chilling Trump plan to seize power permanently.\nFrom Jul 19, 2024 youtu.be/EhZfiIVdoNk?...', "And if you want to run for office, checkout my Substack.  I'm pouring out my huge knowledge base on state/local government & elections to help people who want to change the nature of politics in the US!!!!  It's desperately needed!", 'I said 70% would help, 99% wouldn\'t do anything. Is that 1% worth the risk of what? Alienating men and losing all elections?\nYes. Yes it it. \nNervous is not the same as picking a bear. Nervous is fine. That is caution. Nervous doesn\'t lead people like you to jump to 30% "something happens".', 'Fuck that! If we’re lucky enough to have further elections- this is how we lose', '" “Musk has made numerous posts that have been criticized for promoting or endorsing misinformation, especially related to political events, elections, health issues like COVID-19, and conspiracy theories."', 'Elections should be publicly funded. No private donations. Fact vetted ads.', "We're not doing the texts in Oregon yet (as far as I know). I can check the elections website to make sure my ballot was mailed to me, received and validated.", 'If we have elections in the future…', 'We’re going to survive the next four years. And it all starts with influencing every election between now and then. The midterm elections are our next chance to significantly weaken Dump. #IDissent', 'Who were the 2024 election\'s "crypto voters"? - CBS News\nhttps://www.cbsnews.com/news/who-were-the-2024-elections-crypto-voters-60-minutes/', 'I think we are talking past each other. I am sure the IDP could have been more effective on voter registration drives, GOTV, etc.\nI disagree that mistakes by IDP leaders are the main reason Republicans have been winning more Iowa elections. That reflects a nationwide trend among WWC voters.', "Is it because Tulsi Gabbard knows the democrats are ruining our country.  Now she's helping the man that won two elections(and maybe a 3rd) rebuild what Vice President Joe Biden and his masters broke down.", 'But we’re doomed to 50-50 presidential races for numerous reasons. It sucks. I do think Trump has a unique appeal though so it should be easier assuming we still have fair elections in the future.', 'Yep-the Republicans & corrupt Supreme Court lied repeatedly & under oath about Roe, the elections of 2016, 2020, & 2024, etc. They’ll just keep on lying to get whatever they want. Will the American people will just sit back & let them destroy us like the current Biden admin & DoJ/FBI is doing? Sad!!', "Agreed no reason to think they'd vote liberal, but clearly there are large quantities of people who don't feel that anyone cares about them to turn up and vote.\n\nSomeone who wants to win elections should look into that.", 'lets go in two year increments - mid term elections and the dumpster fire of folks getting fired, quitting, etc and no meaningful legislation getting passed.  pretend we live in switzerland or somewhere', 'The latest Substack from SMART Elections... More data is coming out this week! open.substack.com/pub/smartele...', "We have to fight for fair elections and that American Democracy does not go gently into that good night. \n\nBut if it happens, it's the thing that revolutions are born from. We have a ways to go before we get there and let's hope we never make that trip. \n\nBut we'll do what's necessary if it happens.", 'Important Note: The by-election tracker displayed is a projection and should be viewed as a likely modeled outcome based largely on available public data. Please remember that by-elections are highly unpredictable, and actual results may vary outside predicted Margins of Error.', 'We might be in trouble if they can just flat out buy elections', "If you want to stop voter suppression and have free, fair elections, RUN FOR OFFICE!  I'm pouring out my extensive knowledge base on state/local government to help you do that.  Election calendars for 2025 - 2026 already posted, along with lots of advice for candidates.", "I've been involved in politics long enough to know better but the best candidate doesn't win in a surprising number of elections and that's disappointing.", 'The Canadian analogy breaks down however. Reform started as a regional (western) party and won provincial elections before upsetting the national stage. It didn’t uniformly grab PC votes all across the country. The BQ/PQ grabs a greater portion of seats than SNP.', "People can't even grasp that elections have consequences. Trump voters honestly thought everything was just going to go back to normal after the election. After they did that to us. And we fight to make sure they never see the consequences of their electoral choices. Because we don't want them.", "I see that they care about keeping their base riled up, and they've gone for base elections not cross-party elections and won. I don't think they care about public opinion writ large. They can turn every criticism into fuel to rile up the base. Salvation will not include the maga movement at all.", 'hell fucking no to the high road, since the gop has been stealing elections since at least 2000, and now are currently overthrowing our government/democracy.', 'It’s interesting to think about electoral politics. Presidential elections seem so futile. People hate corporatism yet both parties are corporatist. Somehow Trump convinced people that he is not (or is less) corporatist. Or maybe for populist is a better way to say it.', "Bernie always bad mouths democrats during elections it would be helpful if he didn't broadcast it all over the country", 'We do it here in WA State.\nLove that you can have text messages sent to you: upcoming elections, when your ballot was received, signature authorized, and finally vote counted.', 'Elections have consequences.... Here is the proof.. Beginning to wonder if some  immigrant molested Miller.. So much hate...\n\nwww.axios.com/2024/12/09/t...', 'And the New Jersey Democratic-controlled legislature wonders why the state has been shifting so far to the right in recent elections.  NJ Dems, look in the mirror.', 'Build an organizer core that both persists between elections and serves as a channel for information to percolate up from the ground level', 'You are a partisan. I simply telling you the facts. Obama did abandon the Kurds. He also abandoned Ukraine, West Africa and Syria. \n\nI’m not going to spend 4 yrs outraged at what trump is doing. It also doesn’t win elections', 'Do you genuinely believe that there are going to be any more fair elections, given Russia’s interference in 2016 and 2024? For real question. Who is going to stop him if there aren’t?', "16. Using hackable internet connected voting machines (can't say I can prove there was cheating by the machines) which undermine trust in the elections.", 'Umm, they didn’t vote for them. That’s the problem. I don’t think you’ll out liberal Trump and the GOP to win elections.']
# c2 = ['Noticed an uncanny resemblance and had to whip this up:\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Making a big commitment next year. In 2025, I will make it an effort to watch every #Formula1 and #NASCAR race possible and become a duel fan. Here’s to another season of racing', '2024年F1アブダビGP《決勝》ハイライト動画：数々のアクションの末にマクラーレン渇望のタイトルで幕を閉じた最終戦\n\n🔗 formula1-data.com/article/abu-...\n\n🏷️ #F1jp #F1アブダビGP', 'I am a Verstappen fan\n\n#f1 #formula1 #memes #AbuDhabiGP', '3 months without f1\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Just Chuck doin Chuck things \n\n#f1 #formula1 #memes #AbuDhabiGP', 'Wtf was that camera angle\n\n#f1 #formula1 #memes #AbuDhabiGP', '“Lando, we can be world champions” he said again, this time more firmly\n\n#f1 #formula1 #memes #AbuDhabiGP', 'BLACK FLAG for Max Verstappen\n\n#f1 #formula1 #memes #AbuDhabiGP', '「ハマータイム」で締め括られた伝説―ハミルトンとメルセデスの別れ、12年間の黄金時代に幕\n\n🔗 formula1-data.com/article/hamm...\n\n🏷️ #F1jp #F1アブダビGP #メルセデス #ルイス・ハミルトン', 'Lando Norris raih pole position di #AbuDhabiGP, membawa McLaren di ambang gelar konstruktor pertama setelah 26 tahun! \n\nApakah #McLaren akan sukses musim F1 2024 dengan kemenangan besar?  #F1 #Formula1 #LandoNorris #OscarPiastri #update #news #seketika \nwww.seketika.com/lando-norris...', 'フェルスタッペン、謝罪と批判で見せた温度差の真意―”手遅れ”で至ったピアストリ接触事故\n\n🔗 formula1-data.com/article/coll...\n\n🏷️ #F1jp #F1アブダビGP #レッドブル #マックス・フェルスタッペン #オスカー・ピアストリ', 'Valtteri Bottas 🇫🇮 says that moving to Sauber🇨🇭 was a mistake.\n\nhttps://www.motorsport.com/f1/news/former-f1-race-winner-bottas-labels-his-sauber-career-a-mistake-after-difficult-2024/10680852/?utm_source=RSS&utm_medium=referral&utm_campaign=RSS-F1&utm_term=News&utm_content=www\n\n#F1 #Formula1', 'Fixed it\n\n#f1 #formula1 #memes #AbuDhabiGP', 'what if your name was LEWIS HAMILTON and your car was SHIT and your teammate was crying about his DRAMA with your 2021 RIVAL and so you just leave your team for a new one that will make you MENTALLY UNSTABLE in the long run but regardless forza FERRARI\n\n#f1 #formula1 #memes #AbuDhabiGP', 'McLaren getting stoned in Abu Dhabi\n\n#f1 #formula1 #memes #AbuDhabiGP', 'If Ferrari can address their key weaknesses in 2025, McLaren and Red Bull will struggle to beat them especially with a rejuvenated Lewis Hamilton(clearly not deluded).\n#formula1 #norris #verstappen #leclerc #hamilton #sainz #ferrari #mclaren', 'The Photographer/Blogger of F1, Kym Illman has another great video for you to watch.\n\nHave fun:\n#F1 | #Formula1 \n#KymIllman', 'Do you agree?\n#F1 | #Formula1', 'Congratulations McClaren and Ferrari for rounding out the podiums today and big ups to Norris and McClaren for winning the constructors. I don\'t wanna hear that "RED BULL DOMINANCE" stuff from any F1 fan today. \n\n#formula1 #f1 #mcclaren #ferrari', 'ローソン、2025年のF1参戦「分からない」ペレス後任報道の裏で\n\n🔗 formula1-data.com/article/abud...\n\n🏷️ #F1jp #F1アブダビGP #RB #RBF1 #VCARB #リアム・ローソン', 'Really3D announces end of series.Thanks to this sub for showing me his channel 2 years ago.\n\n#f1 #formula1 #memes #AbuDhabiGP', "He's gonna serve his 5 place grid penalty in the Tour De France, perhaps!\n\n#f1 #formula1 #memes #AbuDhabiGP", "I'm gonna tell my kids that this was the Team Principal of Mclaren when they won their 2024 Constructors Championship\n\n#f1 #formula1 #memes #AbuDhabiGP", 'Graffiti vandals have been busy again at Woking HQ\n#Formula1 #McLarenF1Team #Papaya\n\nVia @F1', 'Hoy en el vivo de YouTube. McLaren campeón del Campeonato de Constructores. Nueva sanción a Max por el lenguaje. Despedidas varias. \n22:30 🇦🇷 - 20:30 🇨🇴 - 19:30 🇲🇽\n¡Suscribite al canal! \n#F1 #Formula1 #F12024 #AbuDhabiGP 🇦🇪\nwww.youtube.com/live/JSX6AbM...', "Now here's something new. In the history of #F1, @pierregasly.bsky.social is the first ever driver to not have caused any damage to his car during an entire #Formula1 season.\n\nCredit: \n* Formula One History \n* BWT Alpine Formula One Team", 'GABRIEL BORTOLETO, depois de ser campeão da Fórmula 3 em 2023, sagrou-se, nesse domingo, dia 08/12, campeão da Fórmula 2 de 2024.\n\nParabéns, #GabrielBortoleto !!!\n\n#Bortoleto #Formula2 #F2 #Formula1 #f1 #F1noBandSports #F1naBand #AbuDhabiGP', "#F1 For the use of the word F*CK, here's what #MaxVerstappen needs to do next Friday. \n(via @ErikvHaren )\n\n#MV33 #FIA #Formula1", 'In his last race for Haas, Kevin Magnussen (Haas VF-24) scored the fastest lap after a switch to Soft tires following an incident with Valtteri Bottas. The Danish driver is signed up to race for BMW in the WEC in 2025.\n\n#f1 #formula1', "Ted's Race Notebook - Abu Dhabi Grand Prix 2024 \n#tedsnotebook #f1 #AbudhabiGP #AbuDhabiGrandPrix #AbuDhabiGrandPrix2024 #AD24 #Formula1", 'Another post to celebrate the end of the season \n\n#formula1 #f1 #funny #comic #art', '12 anos, lewis é o ídolo da mercedes e a mercedes sempre será a casa do lewis, independente dos caminhos tomados  mercedes e hamilton sempre estarão juntos\n 🤝🏁\n#formula1\n#mercedesamgpetronas\n#mercedes \n#lewishamilton', 'Brad Pitt e Javier Bardem gravando cenas para o filme Formula1 em Abu Dhabi.', 'Damson Idris e Brad Pitt durante às filmagens do filme Formula1 em Abu Dhabi. crédito: Getty Images', 'Very late post, but wanted to congratulate Max and redbull for such an incredible season, we’ve had our ups and downs but I’m happy we got to end it with a somewhat note with daddy max coming into the mix plus the 4th WDC!! \n\n#maxverstappen #mv1 #mv33 #redbullracing #f1 #formula1 #fanart #art', "I'm already sad that the 2024 F1 Season is over. I had a lot of fun not only watching the races but witnessing the highs and lows that occured  during the weekend as well.\n\nThe Off-Season is gonna get spicy and I'm looking forward it to it when it happens\n\n#Formula1", 'McLaren wasclearly in cahoots with SATAN HIMSELF this year\n\n#f1 #formula1 #memes #AbuDhabiGP', 'End of season Checo memes!!\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Mario Isola head of Pirelli is cooking in Abu Dhabi… \n\n#f1 #formula1 #memes #AbuDhabiGP', 'Maybe try in Dutch \n\n#f1 #formula1 #memes #AbuDhabiGP', 'sky\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Timeless plaque\n\n#f1 #formula1 #memes #AbuDhabiGP', 'End of an era for Hamilton and Mercedes. \n\n#lewishamilton #formula1', 'Hello Bluesky!!!\n\n#persona3\n#persona4\n#persona5\n#Formula1\n#TheLastOfUs\n#BayernMunich\n#MickSchumacher\n#PlayStation\n#FootballManager\n#Indonesia\n#Atlus\n#Metaphor\n#OnePiece\n\n#promosky', 'La scuola di filosofia Ferrari 2025\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Did I cry when my daughter was born? No. Did I cry when my sister got married? No. Did I cry when Lewis Hamilton finished his last race with Mercedes? Absolutely 💯 \n#formula1 #lewishamilton', 'Resultado do campeonato de pilotos e do campeonato de construtores da temporada de 2024 da Fórmula 1. #Formula1', 'Sometimes life just isn’t fair \n\n#f1 #formula1 #memes #AbuDhabiGP', '"Wow, we have never looked so good"\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Soy Kanaan \n\n#f1 #formula1 #memes #AbuDhabiGP', "I'm really happy for McLaren, but I do wish Ferrari had won the constructors'. It would have been a perfect ending for Carlos.\n#Formula1 #F1", "10 different teams in the top 10 of the constructor's championship, really shows what a competitive season we had.\n\n#f1 #formula1 #memes #AbuDhabiGP", '馬鹿げた連中め！暴言の裏で謝罪、ピアストリが明かすフェルスタッペンの対応―F1アブダビGP 1周目の事故を巡り\n\n🔗 formula1-data.com/article/pias...\n\n🏷️ #F1jp #F1アブダビGP #レッドブル #マックス・フェルスタッペン #オスカー・ピアストリ #マクラーレン', 'The end of an era 😮\u200d💨 #LewisHamilton #formula1 #f1', 'Ladies and gentlemen, your top 3\n\n#f1 #formula1 #memes #AbuDhabiGP', '2024 WCC\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Take a bow Carlos Sainz, fought till the end for the team, sheer commitment from the smooth operator #Formula1 #F1', 'Calendário unificado e completo de 2025 da Fórmula 1, da Fórmula 2, da Fórmula 3 e da F1 Academy. 🏁 #Formula1 #Formula2 #Formula3 #F1Academy', '角田裕毅とローソンを直撃した「不具合と運営ミス」RB最終戦無得点で目標達成できず\n\n🔗 formula1-data.com/article/tsun...\n\n🏷️ #F1jp #F1アブダビGP #RB #RBF1 #VCARB #角田裕毅 #リアム・ローソン', 'Lando llevó a su escudería al título en Abu Dabi. Piastri no pudo ayudarlo porque debió remontar desde el fondo tras un toque con Verstappen. Buena tarea de las Ferrari y de Gasly.\n#F1 #Formula1 #F12024 #Formula12024 #AbuDhabiGP 🇦🇪\nformulamania.com.ar/08/12/2024/u...', 'I would like to sincerely thank the person on r/formula1 who pointed out that the last time McLaren won a WCC was in 1998 before either Lando or Oscar was born. And by "thank", I mean "send the bill for my bottle of special arthritis Tylenol". 🤣\n\nGo Papaya! Hard-fought and well-earned. 🧡', "Lewis Hamilton Parts Ways With Mercedes; Most Successful Driver-Team Partnership In F1 History: It's the end of an era for F1 driver Lewis Hamilton. After 12 seasons with Mercedes, he's saying farewell to join Ferrari. #LewisHamilton #Formula1 #Mercedes", 'dude actually did it, he literally no damaged an entire season 😭😭😭\n\n#f1 #formula1 #memes #AbuDhabiGP', 'フェルスタッペン、キャリア2度目の「社会貢献活動」の詳細が明らかに―会見で罵り言葉\n\n🔗 formula1-data.com/article/vers...\n\n🏷️ #F1jp #F1アブダビGP #レッドブル #マックス・フェルスタッペン', '相次いだクラッチ不具合、角田裕毅「ちゃんと止まれなかった」無得点も”誇り”を胸に4年目を終了 / F1アブダビGP《決勝》2024\n\n🔗 formula1-data.com/article/abud...\n\n🏷️ #F1jp #F1アブダビGP #RB #RBF1 #VCARB #角田裕毅', 'Excited to see what happens next year with Ferrari 🏎️ ✊🏾 #LewisHamilton #Formula1 #F1', 'ペレス、2025年F1シートの不確実性 初めて認める―最終戦リタイヤの裏で語った進退\n\n🔗 formula1-data.com/article/afte...\n\n🏷️ #F1jp #F1アブダビGP #レッドブル #セルジオ・ペレス', '2024年F1第24戦アブダビGP ポイントランキング：マクラーレン年間王者！角田裕毅はキャリア最上12位\n\n🔗 formula1-data.com/article/abud...\n\n🏷️ #F1jp #F1アブダビGP', 'Season wrap-up \n\n#f1 #formula1 #memes #AbuDhabiGP', 'Next year is gonna be painful\n\n#f1 #formula1 #memes #AbuDhabiGP', 'He deserves better...\n\n#f1 #formula1 #memes #AbuDhabiGP', "It's pretty shitty to steal others content without attribution. \n\nThis was made by u/_RichardParry_ and he just posted it to the /r/Formula1 subreddit less than an hour ago.", 'Zak Brown is the G.O.A.T.\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Most Kevin race possible\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Para deixar registrado o resultado do GP de Abu Dhabi: \n\n1) Norris\n2) Sainz\n3) Leclerc\n\n#AbuDhabiGP #Formula1', 'World according to Will Buxton \n\n#f1 #formula1 #memes #AbuDhabiGP', 'Me defending Mercedes and Alpine next season like my life depends on it #F1 #Formula1', '🦎\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Battle of the Papaya  \n\n#f1 #formula1 #memes #AbuDhabiGP', 'Colapinto quedó para la cola\n.\n#Argentina\n#Formula1\n#F1', 'nice finnish to the season\n\n#f1 #formula1 #memes #AbuDhabiGP', 'That was certainly a more interesting season of Formula 1! I was lucky enough to see history made at Silverstone with 3 British drivers qualifying P1,P2 and P3 with Lewis winning on race day! 😄\n\nExcited for next season with some fresh faces and Lewis at Ferrari 🙂 #F12025 #F1 #formula1', '💀\n\n#f1 #formula1 #memes #AbuDhabiGP', 'Late but better than never. \n\n#f1 #formula1 #memes #AbuDhabiGP', 'Following his retirement in the 2024 Abu Dhabi GP, Sergio Perez scored twice as many points this season (152) as Mika Hakkinen (76) in the 1999 season using MP4/14, one of the fastest car in history\n\n#f1 #formula1 #memes #AbuDhabiGP', 'El agradecimiento de Franco Colapinto al equipo Williams por haberle dado la oportunidad de estar en la Fórmula 1.\n#F1 #Formula1 #F12024 #Formula12024 #AbuDhabiGP 🇦🇪', 'Un gesto que refleja la conexión y el respeto entre ellos, y que quedará grabado en la historia del deporte 🙌. ¡Un adiós emotivo a la temporada! \n\n#FrancoColapinto #F1 #AbuDhabi #JamesVowles #Emoción #Deporte #Fórmula1 🏎️💥', 'Caption this WRONG ANSWERS ONLY\n\n#f1 #formula1 #memes #AbuDhabiGP', "This movie I can't 😭\n\n#f1 #formula1 #memes #AbuDhabiGP", 'Congratulations to McLaren! 2024 Constructors is a testament to their development and drivers. Sticking with the dev pattern, roping in Piastri, and Lando were all bold decisions that clearly paid off.  The McLaren team deserves a standing ovation for this incredible achievement! #formula1 #f1', '💪 | Mercedes will keep cheering for Lewis Hamilton, as Toto Wolff said after the 2024 Abu Dhabi Grand Prix. 🤝\n#F1 #Formula1', 'McLaren world champions.\nOnly 96 Day to go and we’re off again. #f1 #formula1 #Mclaren', '[Chris Medland] Lando Norris has been disqualified from the Abu Dhabi Grand Prix. Just kidding next year surely is your year Ferrari fans\n\n#f1 #formula1 #memes #AbuDhabiGP', 'it gets a little longer in a williams.\n\n#f1 #formula1 #memes #AbuDhabiGP', "Yeah apply across the board but posts from today didn't specifically tag/mention F1 or Formula1. Would have to add every driver/team etc. To be honest the initial post was pretty knee jerk. As replied to another, default feed changed now, as nice as it would be still reliant on individuals using it.", 'They wish they had a gasly \n\n#f1 #formula1 #memes #AbuDhabiGP', "Details of Verstappen's 'community service' for swearing revealed #F1 #MaxVerstappen #Formula1 #Motorsport", 'NORRIS WINS AND MCLAREN TAKES THE CONSTRUCTORS CHAMPIONSHIP!!!!!!!! #Formula1', "Surely she's doing it on purpose at this point...\n\n#Formula1 #Offseason"]
#
# clusters = [c1, c2]

def llm_summarize_clusters(clusters):
    for texts in clusters:
        results = summarize_and_generate_key_phrases(texts)

        # Print results
        for i, result in enumerate(results, 1):
            print(f"\nText {i}:")
            print(f"Summary: {result['summary']}")
            print(f"Key Phrases: {result['key_phrases']}")