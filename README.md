# 问题描述：
  本次提交创建了五个通用的prompts模板，包括总结，抽取，对比，计划和审查。模板的设计分层系统模板和用户模板两个层次。
  *   ## 系统模板：
    分为一般性系统模板和问题相关性系统模板。
  *   ### 一般性系统模板
        约束了AI行为的基本准则，明确了AI的工作方式。
  *   ### 问题相关性系统模板
        约束了AI面对具体类别问题时的所扮演的角色和所应承担职责。
  *   ## 用户模板
      明确了AI具体的工作内容，包含了具体的内如内容，用户期待得到的答案细节以及回答所呈现的具体方式。

# 测试：
  *   ## 测试工具
        针对本次提交，使用了molmo-2-8b模型进行测试。
  *   ## 测试内容
        向AI提交一段不超过1000词的英文故事，利用总结模板要求AI生成对该故事的综述。
  *   ## 测试结果:
  *     ### prompts:
        你的职责是从复杂内容中提炼重点。你应当优先保证准确，而不是内容丰富。请总结下面的内容：用简单的话说明整体在讲什么。提炼 3～5 条最重要的信息。不加入原文没有的内容。使用条目形式输出。
  *     ### response:
    **Summary: The Last Light in Maple Street**

      - Every evening at 7:13 p.m., a single streetlight always turned on ahead of the others on Maple Street.
      - Mrs. Carter and Noah, curious about this unusual event, investigated and discovered a hidden metal box behind the light, belonging to Mrs. 
      Carter’s late husband, Edward, who had installed it as a special signal for her.
      - The light had become a meaningful way for Edward to show that she was safe even after his death, helping Mrs. Carter not feel alone at night.
      - The city tried to fix the light but ultimately decided to leave it on as a token of remembrance and to give Mrs. Carter peace of mind.
    
